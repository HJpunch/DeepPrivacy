import requests as rq
import pandas as pd

from typing import Literal


def check_server_status(url:str) -> bool:
    try:
        response = rq.get(url)
    
    except rq.exceptions.ConnectionError:
        return False
    
    else:
        if response.status_code == 200:
            return True
        return False

def read_file(files:list):
    if isinstance(files, list):
        data = [('file', open(f, 'rb')) for f in files]
    else:
        data = [('file', open(files, 'rb'))]
    return data

def post_file(*args, **kwargs) -> dict:
    response = rq.post(*args, **kwargs)
    if response.status_code == 200:
        result_json = response.json()
        return result_json
    else:
        raise ValueError

def get_file(url:str):
    response = rq.get(url)
    return response.content

def get_result(url:str,
               result:dict, 
               mode:Literal['image_detection',
                            'video_detection',
                            'video_recognition']):
    
    if mode == 'image_detection':
        result = result['result']

        for img_name in result.keys():
            img_url = f"{url}/{img_name}"
            img = rq.get(img_url)
            print(f"reponse: {img.status_code}")
            if result[img_name] == []:
                print("None")
                continue
            
            for temp in result[img_name]:
                obj_class = temp['class']
                confidence = temp['conf']
                crop_dir = temp['crop_dir']
                coord = temp['xyxy']

                print(f"img_name: {img_name}\n\
                        class: {obj_class}\n\
                        confidence: {100*confidence:.2f}\n\
                        crop_dir: {crop_dir}\n\
                        coord: {coord}")
            
    elif mode == 'video_detection':
        output_video_dir = result['video_dir']
        fps = result['fps']
        print(f"output_video_dir: {output_video_dir}")

        for i, frame in enumerate(result['result'].keys()):
            sec = f"{i/fps:.4f}"
            exp = f"frame_{i} sec: {sec}"
            print(exp)

            for temp in result['result'][frame]:
                obj_class = temp['class']
                confidence = temp['conf']
                crop_dir = temp['crop_dir']
                coord = temp['xyxy']

                print(f"class: {obj_class}\n\
                        confidence: {100*confidence:.2f}\n\
                        crop_dir: {crop_dir}\n\
                        coord: {coord}")

    elif mode == 'video_recognition':
        csv_save_dir = result['csv_save_dir']
        result = result['result']

        crop_img_dir_list = result['crop_img_dir_list']
        recognize_result = result['recognize']
        video_unique_result = result['video']

        if len(crop_img_dir_list) == 0:
            print("None")
            return
        
        for i, (img_json, video) in enumerate(zip(recognize_result, video_unique_result)):
            crop_img = crop_img_dir_list[i]
            csv = csv_save_dir + f"/result_{i}.csv"
            print(f"crop_img: {crop_img}\ncsv: {csv}", end="\n\n")

            if not video:
                print("None")
                continue
            
            for idx in list(video):
                print(idx)

            df = pd.DataFrame(img_json)
            for row in range(len(df)):
                temp = df.iloc[row]
                img_path = temp['path']
                frame = temp['frame']
                video_name = temp['video']
                conf = temp['theta']

                print(f"image path: {img_path}\n\
                        frame: {frame}\n\
                        video = {video_name}\n\
                        conf = {100*conf:.2f}%")