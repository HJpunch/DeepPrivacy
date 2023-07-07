import requests as rq

def post_request(url:str, json:dict, *args, **kwargs):
    request = rq.post(url=url, json=json, *args, **kwargs)
    result = request.json()['result']

    return result