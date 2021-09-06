import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image

import requests
import math
import io
import json
from PIL import ImageDraw
from PIL import ImageFont

with open('secret.json') as f:
    secret_json = json.load(f)
SUBSCRIPTION_KEY = secret_json['KEY1']
assert SUBSCRIPTION_KEY

face_api_url = secret_json['ENDPOINT'] + 'face/v1.0/detect'

st.title('My 1st app')

st.write('DataFrame')
st.write(
    pd.DataFrame({
        '1st column': [1, 2, 3, 4],
        '2nd column': [5, 6, 7, 8],
    }))
"""
# My 1st App
## 見出しを付ける
- こんな感じでマジックコマンドを使用できます。
- なんとMarkdownに対応しています。
- 文章を書くときにとても便利な機能です。
"""

if st.checkbox('Show DataFrame'):
    chart_df = pd.DataFrame(np.random.randn(20, 3), columns=['a', 'b', 'c'])
    st.line_chart(chart_df)

st.title('画像のアップロード')
uploaded_file = st.file_uploader("Choose an image...", type="jpg")
if uploaded_file is not None:
    img = Image.open(uploaded_file)
    with io.BytesIO() as output:
        img.save(output, format="JPEG")
        binary_img = output.getvalue()  # binary

    headers = {
        'Content-Type': 'application/octet-stream',
        'Ocp-Apim-Subscription-Key': SUBSCRIPTION_KEY
    }

    params = {
        # 'detectionModel': 'detection_03',
        'returnFaceId':
        'true',
        'returnFaceAttributes':
        'age, gender, headPose, smile, facialHair, glasses, emotion, hair, makeup, occlusion, accessories, blur, exposure, noise',
    }

    res = requests.post(
        face_api_url,
        params=params,
        headers=headers,
        # json={"url": image_url},
        data=binary_img)

    results = res.json()

    # 複数人がいた場合にはresultをfor文で回せばよい
    for result in results:
        rect = result['faceRectangle']
        draw = ImageDraw.Draw(img)
        # 画像にお絵描きができる->img
        # draw.line([(0,50),(200,50),(0,150),(200,150)],fill='red',width=5)
        # 顔の位置を緑色で矩形選択
        linewidth = 4  # 線の太さ
        rectcolor = (255, 0, 0)  # 矩形の色(RGB)。red
        draw.rectangle(
            [(rect['left'], rect['top']),
             (rect['left'] + rect['width'], rect['top'] + rect['height'])],
            fill=None,
            outline=rectcolor,
            width=linewidth)

        textcolor = (255, 255, 255)  # テキストの色(RGB)。今回は白色です。
        textsize = 12  # 描画するテキストの大きさ。今回は12px。

        # テキストの描画の準備。"arial.ttf"はフォント名。
        # font = ImageFont.truetype("arial.ttf", size=textsize)

        faceAttributes = result['faceAttributes']
        gender = faceAttributes['gender']
        age = math.floor(faceAttributes['age'])
        text = gender + ' ' + str(age) + 'yo'

        txpos = (rect['left'], rect['top'] - textsize - linewidth // 2
                 )  # テキストの描画を開始する座標
        # x座標はleftと同じ。
        # y座標はtopよりテキストの大きさと矩形の線の太さの半分だけ上にする。
        # テキストの大きさ(=textsize)。矩形の線の太さの半分(=linewidth//2)。

        txw, txh = draw.textsize(text,
                                 #  font=font
                                 )
        # 文字列"text"が占める領域のサイズを取得

        draw.rectangle([txpos, (rect['left'] + txw, rect['top'])],
                       outline=rectcolor,
                       fill=rectcolor,
                       width=linewidth)
        # テキストを描画する領域を"rectcolor"で塗りつぶし。
        # 左上座標をtxpos、右下座標を (left+txw, top)とする矩形をrectcolor(=赤色)で塗りつぶし。

        draw.text(
            txpos,
            text,
            #   font=font,
            fill=textcolor)

    st.image(img, caption='Uploaded image.', use_column_width=True)

# azure quick startを参照しながら

# 画像をバイナリデータに変換する必要あり
# img = Image.open('trick.jpeg')
# with open('trick.jpeg', 'rb') as f:
#     binary_img = f.read()
