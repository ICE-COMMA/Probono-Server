import requests
from config.settings.common import get_env_variable

from probono_app.models import SafetyGuardHouse

class SafetyGuardHouseInfo():

    def __init__(self):
        self.__key = get_env_variable('SAFETY_GUARD_HOUSE_KEY')
        self.__base_url = "http://api.data.go.kr/openapi/tn_pubr_public_female_safety_prtchouse_api"

    def get_safety_guard_house(self):
        start_index = 1
        end_index = 100

        SafetyGuardHouse.objects.all().delete()

        to_insert = []
        while True:
            params = {
                'serviceKey'    : self.__key,
                'pageNo'        : start_index,
                'numOfRows'     : end_index,
                'type'          : 'json'
            }
            response = requests.get(self.__base_url, params=params)
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