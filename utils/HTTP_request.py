import requests as rq


def __read_file(path:str):
    files = open(path, 'rb')
    return {'file': files}

def read_file(files:list):
    data = [('file', open(f, 'rb')) for f in files]
    return data

def post_file(*args, **kwargs):
    return rq.post(*args, **kwargs)

