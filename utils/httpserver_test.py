import sys
import requests

URL = 'http://192.168.1.230:18400/register'

client = requests.session()

client.get(URL)
if 'csrftoken' in client.cookies:
    csrftoken = client.cookies['csrftoken']

else:
    csrftoken = client.cookies['csrf']

register_data = dict(userid='aideep', email='aideep@aideep.ai',
                     password='aideep3030', password_2='aideep3030')

r = client.post(URL, data=register_data, headers=dict(Referer=URL))