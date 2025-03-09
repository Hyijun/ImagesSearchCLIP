# Batch size of images
BATCH_SIZE = 4

# path to .pt file like "clip_cn_vit-h-14.pt"
MODEL_PATH=r"I:\chinese-clip-vit-huge-patch14\clip_cn_vit-h-14.pt"

# path to the images to search
IMAGES_DIR = r"F:\图片\\"

# will the search process scan the subdirectories if IMAGES_DIR
INCLUDE_SUBDIRECTORIES = False

# Processor, should be one of "cuda" or "cpu"
DEVICE_TYPE = "cuda"

# Available models: ['ViT-B-16', 'ViT-L-14', 'ViT-L-14-336', 'ViT-H-14', 'RN50']
VISION_MODEL_NAME = "ViT-H-14"

# "RoBERTa-wwm-ext-base-chinese" unless you are using ViT-H-14, otherwise please choose "RoBERTa-wwm-ext-large-chinese"
TEXT_MODEL_NAME = "RoBERTa-wwm-ext-large-chinese"

# set to 336 if using ViT-L-14-336, otherwise please set to 224
INPUT_RESOLUTION = 224

# HTTP Sever images Root
HTTP_ROOT = "http://localhost/images"

### Milvus configs

# Must be "milvus" or "milvus_lite"
DB_TYPE = "milvus_lite"

# Use URL like "http://localhost:19530" if you are using DB_TYPE = "milvus"
# Use milvus db file path if you are using DB_TYPE = "milvus_lite"
DB_LOCATION = "./milvus_lite.db"

# milvus db name
DB_NAME = "main"

# collection name of db
DB_COLLECTION_NAME = "ViT_H_14_F"

# if you are using "milvus", only "FLAT" can be use
DB_INDEX_TYPE = "FLAT"

# depend on CLIP model you are using
DB_EMB_DIMENSION = 1024

DB_USER = None
DB_PASSWD = None