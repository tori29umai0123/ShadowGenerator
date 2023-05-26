# -*- coding: utf-8 -*-
import base64
import io
import requests
from PIL import Image, ImageFilter
import os
import yaml
import cv2
import datetime
import imread

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
config = yaml.safe_load(open(os.path.join(SCRIPT_DIR, "config.yaml"), "r"))

class ShadowGenerator:
    def __init__(self, base_url=config["base_url"]):
        self.base_url = base_url

    def generate_Shadow(self,max_size,output_dir,image_path,mask_path,prompt):
        init_img = imread.imread(image_path)[:, :, ::-1]
        init_retval, init_bytes = cv2.imencode('.png', init_img)
        init_img = imread.resize_image(init_img,max_size)
        h, w, _ = init_img.shape
        init_images = base64.b64encode(init_bytes).decode('utf-8')
        mask_img = imread.imread(mask_path)[:, :, ::-1]
        mask_retval, mask_bytes = cv2.imencode('.png', mask_img)
        mask_img = imread.resize_image(init_img,max_size)
        mask_images = base64.b64encode(mask_bytes).decode('utf-8')
        
        payload = {
                "init_images": [init_images],
                "mask": mask_images,
                "sd_model": config["sd_model"],
                "prompt": config["base_prompt"] + prompt,
                "negative_prompt": config["negative_prompt"],
                "sampler_name": "Euler a",
                "steps": 20,
                "cfg_scale": 7,
                "batch_count": 1,
                "batch_size": 1,
                "filter_nsfw": False,
                "include_grid": False,
                "width": w,
                "height":h,
                "enable_hr": False,
                "denoising_strength": 1.0,
                "hr_scale": 1.3,
                "seed":-1,
                "alwayson_scripts": {
                    "controlnet": {
                      "args": [
                        {
                        "input_image": init_images,
                        "pixel_perfect": True,
                        "module": "lineart_standard (from white bg & black line)",
                        "model": config["cn_model"],
                        }
                      ]
                    }
                }
            }

        path = "/sdapi/v1/img2img"
        response = requests.post(url=f"{self.base_url}{path}", json=payload)
        r = response.json()
        result = r['images'][0]
        now = datetime.datetime.now()
        filename = output_dir + "/ouput_" + now.strftime("%Y%m%d_%H%M%S") + ".png"
        image = Image.open(io.BytesIO(base64.b64decode(result.split(",", 1)[0])))
        re_img = image.resize((w,h)) 
        re_img.save(filename)
        print(r['info'])
        print("Shadow_Generate done!")
        return filename


def main(max_size,output_dir,image_path,mask_path,prompt):
    Shadow_Generator = ShadowGenerator()
    out_path = Shadow_Generator.generate_Shadow(max_size,output_dir,image_path,mask_path,prompt)
    return out_path

if __name__ == "__main__":
    max_size = 1600
    image_path = "C:/ShadowGenerator/test.png"
    mask_path = "C:/ShadowGenerator/mask.png"
    output_dir = "C:/ShadowGenerator"
    prompt = "1girl"
    out_path = main(max_size,output_dir,image_path,mask_path,prompt)
    print(out_path)