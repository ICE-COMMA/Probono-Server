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

        self.__route_db_name  = 'bus'

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

    def __fetch_data(self, base_url, params):
        response = requests.get(base_url, params=params)
        return response.json()