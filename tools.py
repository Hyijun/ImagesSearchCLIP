from cn_clip.clip import load_from_name, available_models
from CONF import *


def get_model():
    model, preprocess = load_from_name(MODEL_PATH, device=DEVICE_TYPE, vision_model_name=VISION_MODEL_NAME, text_model_name=TEXT_MODEL_NAME, input_resolution=INPUT_RESOLUTION)
    model.eval()
    return model, preprocess