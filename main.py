import torch
from PIL import Image
import torchvision.transforms as tt
from transformers import ChineseCLIPProcessor, ChineseCLIPModel

from CONF import *
from load_images import get_file_paths
from vec_db import get_milvus_client, connect_collection


def calc_image(image_path, processor, model):
    img = Image.open(image_path)
    img_input = processor(images=img, return_tensors="pt").to("cuda")
    img_features = model.get_image_features(**img_input)
    img_features = img_features / img_features.norm(p=2, dim=-1, keepdim=True) # 规范化

    # print(img_features)
    print(img_features.shape)
    print()

    print(img_features.cpu().detach().numpy().tolist())



    return img_features

def test():
    # load clip
    model_path = r"I:\chinese-clip-vit-base-patch16"
    model = ChineseCLIPModel.from_pretrained(model_path,
                                             local_files_only=True,
                                             device_map=0)

    processor = ChineseCLIPProcessor.from_pretrained(model_path,
                                                     local_files_only=True,
                                                     device_map=0)

    # test
    calc_image(r".\\122638766_p0.jpg", processor, model)
    calc_image(r"F:\图片\114842790_p0.jpg", processor, model)
    calc_image(r"F:\图片\QQ图片20221221175615.jpg", processor, model)
    calc_image(r"F:\图片\5f5fd31fbe096b635b9749810e338744eaf8ac6a.jpg", processor, model)
    calc_image(r"F:\图片\QQ图片20190212234142.jpg", processor, model)


    # # text tags
    # texts = ["一个拿着木棍的女孩", "一个拿着木棍的男孩", "一个正在跳舞的女孩", "一幅风景画"]
    # texts_input = processor(text=texts, images=img, return_tensors="pt", padding=True)
    # outputs = model(**texts_input)
    #
    # logit = outputs.logits_per_image
    # probs = logit.softmax(dim=1)
    #
    # print(probs)
    # probs_list = probs.tolist()
    # print(texts[probs_list.index(max(probs_list))])


def main():
    model_path = r"I:\chinese-clip-vit-base-patch16"

if __name__ == '__main__':
    main()
