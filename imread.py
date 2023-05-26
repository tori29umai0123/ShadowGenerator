# -*- coding: utf-8 -*-
import cv2
import numpy as np

#日本語が含まれるファイル名でもcv2で読み込めるコード
def imread(filename, flags=cv2.IMREAD_COLOR, dtype=np.uint8):
    try:
        n = np.fromfile(filename, dtype)
        img = cv2.imdecode(n, flags)
        return img
    except Exception as e:
        print(e)
        return None

#指定したmax_size以下の長辺に収まりつつ画像サイズを16の倍数に丸めるスクリプト
def resize_image(image,max_size):

    # 画像のサイズを取得
    height, width, _ = image.shape

    # 縦横のサイズを16の倍数に丸める
    new_width = round(width / 16) * 16
    new_height = round(height / 16) * 16

    # アスペクト比を保ちつつ長辺がn以内になるようにリサイズ
    aspect_ratio = width / height
    if aspect_ratio >= 1:
        if new_width > max_size:
            new_width = max_size
            new_height = round(new_width / aspect_ratio)
    else:
        if new_height > max_size:
            new_height = max_size
            new_width = round(new_height * aspect_ratio)

    resized_image = cv2.resize(image, (new_width, new_height))
    return resized_image