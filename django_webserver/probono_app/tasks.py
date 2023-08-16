import requests
from celery import shared_task
from config import settings

'''
서버 구동 후, 반드시 터미널 창 두개 열어서 실행해야 함.

celery -A your_project worker -l info
celery -A your_project beat -l info
'''

@shared_task
def get_subway_elvtr_task():
    base_url = 'http://openapi.seoul.go.kr:8088/4f6a5a74796c696d3534425a686562/json/tbTraficElvtr'
    start_index = 1
    end_index = 100

    all_data = []

    while True:
        url = f"{base_url}/{start_index}/{end_index}/"
        response = requests.get(url)
        data = response.json()

        if 'tbTraficElvtr' in data and 'row' in data['tbTraficElvtr']:
            all_data.extend(data['tbTraficElvtr']['row'])

        start_index += 100
        end_index += 100

        if len(data['tbTraficElvtr']['row']) < 100:
            break

    # save to Mongo DB
    # Right here

