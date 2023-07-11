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
    data = [('file', open(f, 'rb')) for f in files]
    return data

def post_file(*args, **kwargs) -> list:
    result = rq.post(*args, **kwargs)
    result_json = result.json()['result']  # image detection.
    # return result_json  # ['data/2023_07_11_14_21_08/output/1.jpg']

    # base64 결과값 디코딩 변환
    for image in result_json.keys():
        image = Image.open(io.BytesIO(image))
        qimage = ImageQt(image)
    return qimage


# image detection
def get_result(result:dict):
    result_json = result.json()['result']
    print(result_json)