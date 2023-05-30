# -*- coding: utf-8 -*-
# https://github.com/kohya-ss/sd-scripts/blob/main/finetune/tag_images_by_wd14_tagger.py

import csv
import os

from PIL import Image
import cv2
import numpy as np
from tensorflow.keras.models import load_model
from huggingface_hub import hf_hub_download
from pathlib import Path

# from wd14 tagger
IMAGE_SIZE = 448

# wd-v1-4-swinv2-tagger-v2 / wd-v1-4-vit-tagger / wd-v1-4-vit-tagger-v2/ wd-v1-4-convnext-tagger / wd-v1-4-convnext-tagger-v2
DEFAULT_WD14_TAGGER_REPO = "SmilingWolf/wd-v1-4-convnext-tagger-v2"
FILES = ["keras_metadata.pb", "saved_model.pb", "selected_tags.csv"]
SUB_DIR = "variables"
SUB_DIR_FILES = ["variables.data-00000-of-00001", "variables.index"]
CSV_FILE = FILES[-1]
model = None

def preprocess_image(image):
    image = np.array(image)
    image = image[:, :, ::-1]  # RGB->BGR

    # pad to square
    size = max(image.shape[0:2])
    pad_x = size - image.shape[1]
    pad_y = size - image.shape[0]
    pad_l = pad_x // 2
    pad_t = pad_y // 2
    image = np.pad(image, ((pad_t, pad_y - pad_t), (pad_l, pad_x - pad_l), (0, 0)), mode="constant", constant_values=255)

    interp = cv2.INTER_AREA if size > IMAGE_SIZE else cv2.INTER_LANCZOS4
    image = cv2.resize(image, (IMAGE_SIZE, IMAGE_SIZE), interpolation=interp)

    image = image.astype(np.float32)
    return image

def modelLoad():
    # hf_hub_downloadをそのまま使うとsymlink関係で問題があるらしいので、キャッシュディレクトリとforce_filenameを指定してなんとかする
    # depreacatedの警告が出るけどなくなったらその時
    # https://github.com/toriato/stable-diffusion-webui-wd14-tagger/issues/22

    model_dir = "wd14_tagger_model"
    repo_id = DEFAULT_WD14_TAGGER_REPO

    if not os.path.exists(model_dir):
        print(f"downloading wd14 tagger model from hf_hub. id: {repo_id}")
        for file in FILES:
            hf_hub_download(repo_id, file, cache_dir=model_dir, force_download=True, force_filename=file)
        for file in SUB_DIR_FILES:
            hf_hub_download(
                repo_id,
                file,
                subfolder=SUB_DIR,
                cache_dir=os.path.join(model_dir, SUB_DIR),
                force_download=True,
                force_filename=file,
            )
    else:
        print("using existing wd14 tagger model")

    # モデルを読み込む
    model = load_model(model_dir)

    return model

def main(image_path,model):

    # label_names = pd.read_csv("2022_0000_0899_6549/selected_tags.csv")
    # 依存ライブラリを増やしたくないので自力で読むよ
    model_dir = "wd14_tagger_model"
    with open(os.path.join(model_dir, CSV_FILE), "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        l = [row for row in reader]
        header = l[0]  # tag_id,name,category,count
        rows = l[1:]
    assert header[0] == "tag_id" and header[1] == "name" and header[2] == "category", f"unexpected csv format: {header}"

    general_tags = [row[1] for row in rows[1:] if row[2] == "0"]
    character_tags = [row[1] for row in rows[1:] if row[2] == "4"]

    tag_freq = {}
    undesired_tags = ["monochrome","lineart","greyscale"]

    def run_batch(path_imgs,model):
        imgs = np.array([im for _, im in path_imgs])
        probs = model(imgs, training=False)
        probs = probs.numpy()

        for (image_path, _), prob in zip(path_imgs, probs):
            # 最初の4つはratingなので無視する
            # # First 4 labels are actually ratings: pick one with argmax
            # ratings_names = label_names[:4]
            # rating_index = ratings_names["probs"].argmax()
            # found_rating = ratings_names[rating_index: rating_index + 1][["name", "probs"]]

            # それ以降はタグなのでconfidenceがthresholdより高いものを追加する
            # Everything else is tags: pick any where prediction confidence > threshold
            combined_tags = []
            general_tag_text = ""
            character_tag_text = ""
            thresh = 0.35 
            for i, p in enumerate(prob[4:]):
                if i < len(general_tags) and p >= thresh:
                    tag_name = general_tags[i]
                    if tag_name not in undesired_tags:
                        tag_freq[tag_name] = tag_freq.get(tag_name, 0) + 1
                        general_tag_text += ", " + tag_name
                        combined_tags.append(tag_name)
                elif i >= len(general_tags) and p >= thresh:
                    tag_name = character_tags[i - len(general_tags)]
                    if tag_name not in undesired_tags:
                        tag_freq[tag_name] = tag_freq.get(tag_name, 0) + 1
                        character_tag_text += ", " + tag_name
                        combined_tags.append(tag_name)

            # 先頭のカンマを取る
            if len(general_tag_text) > 0:
                general_tag_text = general_tag_text[2:]
            if len(character_tag_text) > 0:
                character_tag_text = character_tag_text[2:]

            tag_text = ", ".join(combined_tags)
            return tag_text

    b_imgs = []
    image = Image.open(image_path)
    if image.mode != "RGB":
        image = image.convert("RGB")
    image = preprocess_image(image)
    b_imgs.append((image_path, image))
    tag = run_batch(b_imgs,model)
    return tag

if __name__ == "__main__":
    image_path = "C:/ShadowGenerator/test.png"
    main(image_path)