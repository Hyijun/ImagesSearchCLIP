import os
import json
import asyncio
from collections import deque
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from typing import List
from pathlib import Path
from werkzeug.utils import secure_filename  # pip install werkzeug

from CONF import HTTP_ROOT
from vec_db import MilvusDB
from text2vec import get_text_features, query_in_db
from tools import get_model
import urllib.parse

# 全局配置
NEW_IMAGES_DIR = Path("./uploaded_images")  # 图片上传存储路径
NEW_IMAGES_DIR.mkdir(exist_ok=True)

app = FastAPI()

# 全局任务队列和同步锁
pending_tasks = deque()
processing_lock = asyncio.Lock()


async def process_tasks():
    """后台任务处理循环"""
    while True:
        async with processing_lock:  # 确保串行执行
            if not pending_tasks:
                await asyncio.sleep(0.1)
                continue
            task = pending_tasks.popleft()

            try:
                # 调用搜索函数（假设是同步函数）
                loop = asyncio.get_event_loop()
                results = await loop.run_in_executor(
                    None, search_images, task["text"], task["limit"]
                )
                # 发送结果
                await task["response_queue"].put({"type": "result", "data": results})
            except Exception as e:
                await task["response_queue"].put({"type": "error", "data": str(e)})

            # 通知剩余任务更新队列位置
            for idx, remaining_task in enumerate(pending_tasks):
                await remaining_task["response_queue"].put({"type": "position", "data": idx})


@app.get("/search")
async def search_endpoint(search: str, limit: int):
    """SSE 图片搜索接口"""
    response_queue = asyncio.Queue()
    task = {
        "text": search,
        "limit": limit,
        "response_queue": response_queue
    }
    pending_tasks.append(task)
    initial_position = len(pending_tasks) - 1
    await response_queue.put({"type": "position", "data": initial_position})

    async def event_generator():
        """SSE 事件生成器"""
        while True:
            message = await response_queue.get()
            if message["type"] == "position":
                yield f"data: {json.dumps({'position': message['data']})}\n\n"
            elif message["type"] == "result":
                yield f"data: {json.dumps({'urls': message['data']})}\n\n"
                break
            elif message["type"] == "error":
                yield f"event: error\ndata: {json.dumps({'message': message['data']})}\n\n"
                break

    return StreamingResponse(event_generator(), media_type="text/event-stream")


@app.post("/update")
async def update_endpoint(files: List[UploadFile] = File(...)):
    """批量上传图片接口"""
    for file in files:
        filename = secure_filename(file.filename)
        if not filename:
            continue
        filepath = NEW_IMAGES_DIR / filename

        # 异步写入文件
        content = await file.read()
        with open(filepath, "wb") as f:
            f.write(content)

    return {"status": "success", "uploaded": len(files)}


@app.on_event("startup")
async def startup_event():
    """启动后台任务处理器"""
    asyncio.create_task(process_tasks())

MODEL, PREPROCESS = None, None
milvus_db = MilvusDB()

def load_model():
    global MODEL, PREPROCESS
    MODEL, PREPROCESS = get_model()


def search_images(text: str, limit: int) -> List[str]:
    if MODEL is None or PREPROCESS is None:
        load_model()
    text_features = get_text_features(text, MODEL)
    results = query_in_db(text_features.detach().cpu().numpy().tolist(), milvus_db, limit)
    return [f"{HTTP_ROOT}/{urllib.parse.quote(os.path.basename(image_name))}" for image_name in results]

