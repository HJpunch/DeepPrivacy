import base64
import io
import os
import requests as rq


def read_file(files:list):
    if isinstance(files, list):
        data = [('file', open(f, 'rb')) for f in files]
    else:
        data = [('file', open(files, 'rb'))]
    return data

def post_file(*args, **kwargs) -> dict:
    result = rq.post(*args, **kwargs)  # <Response[200]>
    result_json = result.json()
    return result_json

# image detection
def get_result(result:dict):
    result_json = result.json()['result']
    print(result_json)