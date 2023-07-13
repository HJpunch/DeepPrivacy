import base64
import io
import os
import requests as rq

from PIL import Image
from PIL.ImageQt import ImageQt

def __read_file(path:str):
    files = open(path, 'rb')
    return {'file': files}

def read_file(files:list):
    if isinstance(files, list):
        data = [('file', open(f, 'rb')) for f in files]
    else:
        data = [('file', open(files, 'rb'))]
    return data

def post_file(*args, **kwargs) -> dict:
    result = rq.post(*args, **kwargs)  # <Response[200]>
    result_json = result.json()['result']  # image detection.  {'img_name': ['class coord']}

    # for img_name in result_json.keys():
    #     for idx, temp in enumerate(result_json[img_name]):
    #         obj_class = temp["class"]
    #         accuracy = temp["conf"]
    #         coord = temp["xyxy"]

    #         print(obj_class, accuracy, coord)
    return result_json

    # base64 결과값 디코딩 변환
    for image in result_json.keys():
        image = Image.open(io.BytesIO(image))
        qimage = ImageQt(image)
    return qimage

# image detection
def get_result(result:dict):
    result_json = result.json()['result']
    print(result_json)