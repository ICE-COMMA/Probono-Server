import requests
from celery import shared_task
from config import settings, utils
from .models import SafetyGuardHouse, SubwayElevator, Bus

'''
서버 구동 후, 반드시 터미널 창 두개 열어서 실행해야 함.

celery -A your_project worker -l info
celery -A your_project beat -l info
'''

# db_handle = utils.db_handle
# get_collection = utils.get_collection_handle


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
    SubwayElevator.objects.all().delete()
    to_insert= []
    for data in all_data:
        sw_nm = data.get('SW_NM', '')
        node_wkt = data.get('NODE_WKT', '')
        coordinates = node_wkt.replace("POINT(", "").replace(")", "").split()
        x = coordinates[0]
        y = coordinates[1]
        subway_elevator = SubwayElevator(sw_nm=sw_nm, x=float(x), y=float(y))
        to_insert.append(subway_elevator)
    SubwayElevator.objects.bulk_create(to_insert)
    return


@shared_task
def get_bus_no_to_route():
    base_url = 'http://openapi.seoul.go.kr:8088/57636d66616c696d3536664b555850/json/busRoute'
    start_index = 1
    end_index = 100

    all_data = []
    while True:
        url = f"{base_url}/{start_index}/{end_index}/"
        response = requests.get(url)
        data = response.json()
        if 'busRoute' in data and 'row' in data['busRoute']:
            all_data.extend(data['busRoute']['row'])
        start_index += 100
        end_index += 100
        if len(data['busRoute']['row']) < 100:
            break

    # save to Mongo DB
    Bus.objects.all().delete()
    to_insert = []
    for data in all_data:
        bus_no = data.get('ROUTE', '')
        route = data.get('ROUTE_ID', '')
        no_to_route = Bus(bus_no=bus_no, route=route)
        to_insert.append(no_to_route)
    Bus.objects.bulk_create(to_insert)

    return

@shared_task
def get_safety_guard_house():
    base_url = "http://api.data.go.kr/openapi/tn_pubr_public_female_safety_prtchouse_api"
    start_index = 1
    end_index = 100

    SafetyGuardHouse.objects.all().delete()

    to_insert = []
    while True:
        params = {'serviceKey': 'z3tbVitFT7XffZ43RQ9sMyE0ALiv+EtqOysMUKPdg9E5zTIL3lNVHqGCOS9vPqq73zYw6OhwHiskVZj4MYCJ0w==',
                  'pageNo': start_index,
                  'numOfRows': end_index,
                  'type': 'json'}
        response = requests.get(base_url, params=params)
        data = response.json()

        if 'response' in data and 'body' in data['response'] and 'items' in data['response']['body']:
            items = data['response']['body']['items']
            for target in items:
                if target['ctprvnNm'] == '서울특별시':
                    name = target.get('storNm', '')
                    x = target.get('longitude', '')
                    y = target.get('latitude', '')
                    safety_guard_house = SafetyGuardHouse(name=name, x=float(x), y=float(y))
                    to_insert.append(safety_guard_house)
            if len(items) < 100:
                break
        else:
            break
        start_index += 1
    # print(to_insert)
    # print(len(to_insert))
    SafetyGuardHouse.objects.bulk_create(to_insert)

    return


@shared_task
def update_special_weather_task():
    special_weather = SpecialWeather()
    special_weather.update_special_weather()
    return


@shared_task
def update_demo_task():
    demo = DemoInfo()
    demo._crawling_demo()
    return