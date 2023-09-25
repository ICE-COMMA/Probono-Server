import requests

class Bus_info():
    
    def __init__(self):
        self.base_url = 'http://ws.bus.go.kr/api/rest/buspos/getBusPosByRtid'
        self.key = '4cwiloFmPQxO3hXwmJy3jruoPPh6m8PQZqxBkWecSAgIIeRjq6UIdo0r7ZnmT4Rm4kVErRaD9jd1XU5CS7Chwg=='
        self.bus_type = {'0': False, '1': True, '2': False}
        self.bool = {'0': False, '1': True}

    def get_bus_pos(self, route_id):
        params = {'serviceKey': self.key,
                  'busRouteId': route_id, 'resultType': 'json'}
        data = self.fetch_data(params)
        data = data['msgBody']['itemList']
        ret = []
        for temp_data in data:
            temp = {
                'is_low': self.bus_type.get(temp_data['busType']),
                'is_bus_stopped': self.bool.get(temp_data['stopFlag']),
                'is_full': self.bool.get(temp_data['isFullFlag']),
                'is_last': temp_data['islastyn'],
                'congestion': temp_data['congetion'],
                'next_station_id': temp_data['nextStId'],
                'next_time': temp_data['nextStTm']
            }
            ret.append(temp)
        print(ret)
        return ret

    def fetch_data(self, params):
        response = requests.get(self.base_url, params=params)
        return response.json()