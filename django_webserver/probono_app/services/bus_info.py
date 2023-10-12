import requests
from probono_app.models import Bus

class BusInfo():
    
    def __init__(self):
        self.__pos_base_url   = 'http://ws.bus.go.kr/api/rest/buspos/getBusPosByRtid'
        self.__pos_key        = '4cwiloFmPQxO3hXwmJy3jruoPPh6m8PQZqxBkWecSAgIIeRjq6UIdo0r7ZnmT4Rm4kVErRaD9jd1XU5CS7Chwg=='
        self.__pos_bus_type   = {
            '0' : False,
            '1' : True,
            '2' : False
        }
        self.__pos_bool       = {
            '0' : False,
            '1': True
        }

        self.__route_base_url = 'http://ws.bus.go.kr/api/rest/busRouteInfo/getStaionByRoute'
        self.__route_key      = '4cwiloFmPQxO3hXwmJy3jruoPPh6m8PQZqxBkWecSAgIIeRjq6UIdo0r7ZnmT4Rm4kVErRaD9jd1XU5CS7Chwg=='

        self.__no_to_route_key      = '57636d66616c696d3536664b555850'
        self.__no_to_route_base_url = f'http://openapi.seoul.go.kr:8088/{self.__no_to_route_key}/json/busRoute'

    def get_bus_pos(self, route_id):
        params = {
                    'serviceKey'    : self.__pos_key,
                    'busRouteId'    : route_id,
                    'resultType'    : 'json'
        }
        data = self.__fetch_data(self.__pos_base_url, params)
        data = data['msgBody']['itemList']
        ret = []
        for temp_data in data:
            temp = {
                'is_low'            : self.__pos_bus_type.get(temp_data['busType']),
                'is_bus_stopped'    : self.__pos_bool.get(temp_data['stopFlag']),
                'is_full'           : self.__pos_bool.get(temp_data['isFullFlag']),
                'is_last'           : temp_data['islastyn'],
                'congestion'        : temp_data['congetion'],
                'next_station_id'   : temp_data['nextStId'],
                'next_time'         : temp_data['nextStTm']
            }
            ret.append(temp)
        print(ret)
        return ret

    def get_bus_route(self, bus_num):
        bus_info = Bus.objects.filter(bus_no=bus_num).first()
        
        params = {
            'ServiceKey'    : self.__route_key,
            'busRouteId'    : bus_info.route,
            'resultType'    : 'json'
        }

        data        = self.__fetch_data(self.__route_base_url, params)
        item_list   = data['msgBody']['itemList']

        ret = []
        for target in item_list:
            route_id = target['busRouteId']
            data = {
                'station_id'    : target['station'],
                'name'          : target['stationNm'],
                'seq'           : target['seq'],
                'x'             : target['gpsX'],
                'y'             : target['gpsY']
            }
            print(data)
            ret.append(data)
        return route_id, ret

    def get_bus_no_to_route(self):
        start_index = 1
        end_index = 100

        all_data = []
        while True:
            url = f"{self.__no_to_route_base_url}/{start_index}/{end_index}/"
            response = requests.get(url)
            data = response.json()
            if 'busRoute' in data and 'row' in data['busRoute']:
                all_data.extend(data['busRoute']['row'])
            start_index += 100
            end_index += 100
            if len(data['busRoute']['row']) < 100:
                break

        Bus.objects.all().delete()
        to_insert = []
        for data in all_data:
            bus_no = data.get('ROUTE', '')
            route = data.get('ROUTE_ID', '')
            no_to_route = Bus(bus_no=bus_no, route=route)
            to_insert.append(no_to_route)
        Bus.objects.bulk_create(to_insert)
        return

    def __fetch_data(self, base_url, params):
        response = requests.get(base_url, params=params)
        return response.json()