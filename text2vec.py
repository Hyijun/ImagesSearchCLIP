import torch
from vec_db import *
from tools import *
import cn_clip.clip as clip


def get_text_features(text, model):
    text = clip.tokenize([text]).to(DEVICE_TYPE)

    with torch.no_grad():
        text_features = model.encode_text(text)
        text_features /= text_features.norm(dim=-1, keepdim=True)

        return text_features


def query_in_db(text_features, milvus_db: MilvusDB, limit=10):
    return milvus_db.search_db(text_features, limit=limit)

def main():
    model, preprocess = get_model()
    milvus_db = MilvusDB()

    while True:
        print("请输入要向量化的文本：", end="")
        text = input()
        print("正在计算向量：" + text)
        result = get_text_features(text, model)
        print(query_in_db(result.detach().cpu().numpy().tolist(), milvus_db))


if __name__ == '__main__':
    main()
