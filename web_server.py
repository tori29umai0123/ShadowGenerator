import ShadowGenerator
import mask
import os
import random
import string
import tagger
from flask import Flask, render_template, request, send_file

app = Flask(__name__)


def save_image(file,filename):
    if file:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        return file_path

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/generate_shadow', methods=['POST'])
def generate_shadow():
    image_file = request.files['image']
    mask_file = request.files['mask']
    prompt = request.form['prompt']
    max_size = int(request.form['max_size'])
    filename = 'tmp.png'
    maskname = 'mask.png'

    # 画像の保存処理
    image_path = save_image(image_file,filename)
    mask_path = save_image(mask_file,maskname)

    # 出力画像の保存先
    output_dir = app.config['OUTPUT_FOLDER']

    # ジェネレーター呼び出し
    out_path = ShadowGenerator.main(max_size, output_dir, image_path, mask_path, prompt)

    # 画像を返す
    return send_file(out_path, mimetype='image/png')


@app.route('/parse_prompt', methods=['POST'])
def parse_prompt():
    image_file = request.files['image']
    filename = 'tmp.png'

    # 画像の保存処理
    image_path = save_image(image_file,filename)

    # 生成したタグをそのまま返す
    return tagger.main(image_path)


@app.route('/generate_mask', methods=['POST'])
def generate_mask():
    image_file = request.files['image']
    maskname = 'mask.png'

    # 画像の保存処理
    image_path = save_image(image_file,maskname)

    # マスク画像生成
    masked_path = os.path.join(app.config['UPLOAD_FOLDER'], maskname)
    mask.main(image_path,masked_path);

    # マスク画像を返す
    return send_file(masked_path, mimetype='image/png')

if __name__ == '__main__':
    app.config['UPLOAD_FOLDER'] = 'uploads'
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.mkdir(app.config['UPLOAD_FOLDER'])
    app.config['OUTPUT_FOLDER'] = 'outputs'
    if not os.path.exists(app.config['OUTPUT_FOLDER']):
        os.mkdir(app.config['OUTPUT_FOLDER'])
    app.run()
