import requests
from django_webserver.config.settings.common import get_env_variable

from probono_app.models import SubwayElevator

class SubwayInfo():

    def __init__(self):
        self.__key  = get_env_variable('SUBWAY_ELVTR_KET')
    
    def get_subway_elvtr_task(self):
        base_url = f'http://openapi.seoul.go.kr:8088/{self.__key}/json/tbTraficElvtr'
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
