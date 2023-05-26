# ShadowGenerator
AUTOMATIC1111版Stable Diffusion web UIと連携して、ほぼ全自動で線画から陰影をAIに描画させるツール
![1](https://github.com/tori29umai0123/ShadowGenerator/assets/72191117/e19122c1-00c2-4037-a252-1e6cdc0c246f)

# 使い方
①AUTOMATIC1111版Stable Diffusion web UIのローカル環境を作る<br>
https://github.com/AUTOMATIC1111/stable-diffusion-webui

②controlnetを導入する<br>
https://github.com/Mikubill/sd-webui-controlnet<br>
自分はSD2.1系モデルを使っているので、モデルは以下のcannyを使用。別に1.5系のlineArtとかでも動くと思います。<br>
https://huggingface.co/thibaud/controlnet-sd21/tree/main

③config.yamlをテキストエディタで開いて編集<br>
base_url: 基本弄らなくてよし<br>
sd_model: 使っているStable Diffusionのモデルを指定<br>
cn_model: 使っているControlNetのモデルを指定<br>
base_prompt: デフォルトpromptを設定。基本弄らなくてよし<br>
negative_prompt: ネガティブプロンプトを設定。『Mayng』等のembedding等を使う時は事前に導入しておくこと<br>

④適当な場所にコマンドプロンプトから環境を構築
```
cd C:\
git clone https://github.com/tori29umai0123/ShadowGenerator/
cd C:\ShadowGenerator
python -m venv env
env\Scripts\activate.bat
pip install Pillow
pip install opencv-python
pip install numpy
python -m pip install "tensorflow<2.11"
pip install  keras
pip install huggingface-hub
pip install flask
```
④事前にStable Diffusionを起動しておき、web_server.batを実行。以下のURLをブラウザから開く<br>
http://127.0.0.1:5000/

⑤ブラウザから各種設定して陰影生成<br>
Image Upload：線画<br>
Mask Upload:マスク画像。自動的に生成されるが気に入らなかったら手動でアップロードできる<br>
Parse Prompt：prompt自動生成。手動で設定もできる。<br>
Max Size:生成される画像サイズ<br>
Shadow Generate：上記の設定が終わった後、クリックすると影が生成される<br>
