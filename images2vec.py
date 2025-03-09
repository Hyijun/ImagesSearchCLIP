import torch
from PIL import Image
from transformers import ChineseCLIPModel, ChineseCLIPProcessor
from CONF import BATCH_SIZE, IMAGES_DIR, INCLUDE_SUBDIRECTORIES
from load_images import get_file_paths
from vec_db import MilvusDB


def process_images(images: list, processor, model):
    img_input = processor(images=images, return_tensors="pt").to("cuda")
    img_features = model.get_image_features(**img_input)
    img_features = torch.nn.functional.normalize(img_features, p=2, dim=1) # 规范化

    return img_features

def get_features_with_path(images_path, processor, model, batch_size):
    for file_paths in get_file_paths(images_path, batch_size, extensions=['jpg', 'jpeg', 'png', 'gif'], case_sensitive=False, include_subdirectories=INCLUDE_SUBDIRECTORIES):
        try:
            images_objs = [Image.open(images_file) for images_file in file_paths]
        except Exception as e:
            print(e)
            continue

        try:
            image_features_in_cpu = process_images(images_objs, processor, model).cpu().detach().numpy().tolist()
            yield file_paths, image_features_in_cpu
        except Exception as e:
            print(e)
            continue


def put_text_features_to_db(images_dir, model, processor, milvus_db:MilvusDB):
    for file_paths, img_features in get_features_with_path(images_dir, processor, model, batch_size=BATCH_SIZE):
        milvus_db.insert_db(img_features, file_paths)

def main():
    milvus_db = MilvusDB()
    model_path = r"I:\chinese-clip-vit-huge-patch14"
    model = ChineseCLIPModel.from_pretrained(model_path,
                                             local_files_only=True,
                                             device_map=0)

    preprocess = ChineseCLIPProcessor.from_pretrained(model_path,
                                                     local_files_only=True,
                                                     device_map=0)

    put_text_features_to_db(IMAGES_DIR, model, preprocess, milvus_db)

if __name__ == '__main__':
    main()