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

#指定したmax_size以下の長辺に収めつつアスペクト比を保つスクリプト
def resize_image(image,max_size):

    # 画像のサイズを取得
    height, width, _ = image.shape

    if width % 8 == 0 and height % 8 == 0:
        return

    # 画像のサイズを8の倍数に丸める
    new_width = round(width / 8) * 8
    new_height = round(height / 8) * 8

    # アスペクト比を保ちつつ長辺がmax_size以内になるようにリサイズ
    aspect_ratio = width / height
    if aspect_ratio >= 1:
        if width >height:
            new_width = max_sizeint()
            new_height = int(round(new_width / aspect_ratio))
    else:
        if height > width:
            new_height = max_size
            new_width = round(new_height * aspect_ratio)

    resized_image = cv2.resize(image, (new_width, new_height))
    return resized_image