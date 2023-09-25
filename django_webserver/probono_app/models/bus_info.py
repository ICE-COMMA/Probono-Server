import requests

from config import utils

db_handle = utils.db_handle
get_collection = utils.get_collection_handle

class BusInfo():
    
    def __init__(self):
        self.pos_base_url   = 'http://ws.bus.go.kr/api/rest/buspos/getBusPosByRtid'
        self.pos_key        = '4cwiloFmPQxO3hXwmJy3jruoPPh6m8PQZqxBkWecSAgIIeRjq6UIdo0r7ZnmT4Rm4kVErRaD9jd1XU5CS7Chwg=='
        self.pos_bus_type   = {
            '0' : False,
            '1' : True,
            '2' : False
        }
        self.pos_bool       = {
            '0' : False,
            '1': True
        }

        self.route_base_url = 'http://ws.bus.go.kr/api/rest/busRouteInfo/getStaionByRoute'
        self.route_key      = '4cwiloFmPQxO3hXwmJy3jruoPPh6m8PQZqxBkWecSAgIIeRjq6UIdo0r7ZnmT4Rm4kVErRaD9jd1XU5CS7Chwg=='
        self.route_db_name  = 'bus'

    def get_bus_pos(self, route_id):
        params = {
                    'serviceKey'    : self.pos_key,
                    'busRouteId'    : route_id,
                    'resultType'    : 'json'
        }
        data = self.fetch_data(self.pos_base_url, params)
        data = data['msgBody']['itemList']
        ret = []
        for temp_data in data:
            temp = {
                'is_low'            : self.pos_bus_type.get(temp_data['busType']),
                'is_bus_stopped'    : self.pos_bool.get(temp_data['stopFlag']),
                'is_full'           : self.pos_bool.get(temp_data['isFullFlag']),
                'is_last'           : temp_data['islastyn'],
                'congestion'        : temp_data['congetion'],
                'next_station_id'   : temp_data['nextStId'],
                'next_time'         : temp_data['nextStTm']
            }
            ret.append(temp)
        print(ret)
        return ret

    def get_bus_route(self, bus_num):
        collection_bus  = get_collection(db_handle, self.route_db_name)
        bus_info        = collection_bus.find_one({'bus_no': bus_num})
        
        params = {
            'ServiceKey'    : self.route_key,
            'busRouteId'    : bus_info['route'],
            'resultType'    : 'json'
        }

        data        = self.fetch_data(self.route_base_url, params)
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

    def fetch_data(self, base_url, params):
        response = requests.get(base_url, params=params)
        return response.json()