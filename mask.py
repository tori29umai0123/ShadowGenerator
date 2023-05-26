# -*- coding: utf-8 -*-
import cv2
import numpy as np
import imread

def main(image_path,mask_path):
    # 線画を読み込む
    img_origin = imread.imread(image_path)

    # 白黒反転する
    img = cv2.bitwise_not(img_origin)

    # グレスケにする
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 二値化する
    ret, img_binary = cv2.threshold(img_gray, 0, 255,cv2.THRESH_BINARY)

    # 輪郭抽出する。
    contours, _ = cv2.findContours(img_binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 面積が最大の輪郭を取得する
    contour = max(contours, key=lambda x: cv2.contourArea(x))

    # マスクを作成し保存
    mask = np.zeros_like(img_binary)
    cv2.drawContours(mask, [contour], -1, color=255, thickness=-1)
    cv2.imwrite(mask_path, mask)


if __name__ == "__main__":
    image_path = "C:/ShadowGenerator/test.png"
    main(image_path)