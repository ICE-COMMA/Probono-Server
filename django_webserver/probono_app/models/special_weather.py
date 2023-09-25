import requests
import logging
from pytz import timezone
from datetime import datetime, timedelta
from itertools import groupby


logger = logging.getLogger(__name__)

from config import utils

db_handle = utils.db_handle
get_collection = utils.get_collection_handle

class SpecialWeather():
    
    tmfc1_value = None

    def __init__(self):
        self.base_url   = 'https://apihub.kma.go.kr/api/typ01/url/wrn_met_data.php'
        self.key        = 'm4y76-4OTnaMu-vuDg525w'
        self.params = {
            'wrn'       : 'A',      'reg'   : None,
            'tmfc1'     : None,     'disp'  : '0',
            'authKey'   : self.key
        }
        self.db_name = 'special_weather'
        self.target_reg = [
            ['L1100100', '서울동남권'], ['L1100200', '서울동북권'],
            ['L1100300', '서울서남권'], ['L1100400', '서울서북권']
        ]
        self.wrn = {
            'W' : '강풍', 'R'   : '호우', 'C'   : '한파',
            'D' : '건조', 'O'   : '해일', 'N'   : '지진해일',
            'V' : '풍랑', 'T'   : '태풍', 'S'   : '대설',
            'Y' : '황사', 'H'   : '폭염'
        }
        self.lvl = {
            '1' :   '예비',
            '2' :   '주의보',
            '3' :   '경보'
        }

    def init_special_weather(self):
        print('Initializing Special Weather.. ', end='')
        collection = get_collection(db_handle, self.db_name)
        collection.delete_many({})
        to_insert = self._process_weather_data(self.init_fetch_data)
        if to_insert:
            collection.insert_many(to_insert)
        print('OK')

    def update_special_weather(self):
        print('Updating Special Weather.. ', end='')
        collection = get_collection(db_handle, self.db_name)
        new_data = self._process_weather_data(self.update_fetch_data)
        for target in new_data:
            target_db = collection.find_one(target['WRN'])
            if not target_db:
                collection.delete_one(target_db)
                if target['CMD'] != '3':
                    collection.insert_one(target)
        print('OK')

    def _process_weather_data(self, fetch_method):
        processed_data = []
        for target in self.target_reg:
            ret_fetched_data = fetch_method(target)
            if not ret_fetched_data[1]:
                print('Error!')
                return []
            content_str = ret_fetched_data[0]
            all_data = self.parse_data(content_str, target)
            all_data.sort(key=lambda x: (x['WRN'], x['TM_EF']))
            grouped_data = {key: list(group) for key, group in groupby(all_data, key=lambda x: x['WRN'])}
            processed_data.extend(self.process_grouped_data(grouped_data, target))
        return processed_data


    def init_fetch_data(self, target):
        return self.fetch_data(target, is_initial=True)

    def update_fetch_data(self, target):
        return self.fetch_data(target)

    def set_params(self, target):
        self.params['reg'] = target[0]
        self.params['tmfc1'] = SpecialWeather.tmfc1_value
        return self.params

    def fetch_data(self, target, is_initial=False):
        if is_initial:
            SpecialWeather.tmfc1_value = self.two_months_ago()
            
        params = self.set_params(target)
        SpecialWeather.tmfc1_value = datetime.now().strftime('%Y%m%d%H%M')
        
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            return response.content.decode('utf-8'), True
        except requests.exceptions.HTTPError as http_err:
            if response.status_code == 500:
                print("Internal Server Error : Special weather API server.")
            else:
                print(f"HTTP Error : {http_err}")
        except requests.exceptions.RequestException as req_err:
            print(f"Request Error : {req_err}")
        except Exception as e:
            print(f"Error : {e}")
            print(response)
        return response.content.decode('utf-8'), False

    def parse_data(self, content_str, target):
        content_str = content_str.replace(
            "#START7777", "").replace("#7777END", "").strip()
        lines = content_str.split('\n')
        all_data = []
        for line in lines:
            if line.startswith("#"):
                continue
            fields = line.split(',')
            if len(fields) < 2:
                logger.error(f"Unexpected fields data: {fields}")
                raise ValueError("Insufficient data in fields!")
            tm_ef = datetime.strptime(fields[1].strip(), "%Y%m%d%H%M")
            data = {
                'TM_EF': tm_ef,
                'REG_NM': target[1],
                'WRN': fields[5].strip(),
                'LVL': fields[6].strip(),
                'CMD': fields[7].strip(),
            }
            all_data.append(data)
        return all_data

    def process_grouped_data(self, grouped_data, target):
        to_insert = []

        for w, group in grouped_data.items():
            if group[-1]['CMD'] != '3':
                result = {
                    'TM_EF': group[-1]['TM_EF'],
                    'REG_NM': target[1],
                    'WRN': self.wrn[w],
                    'LVL': self.lvl[group[-1]['LVL']]
                }
                to_insert.append(result)
        return to_insert

    def two_months_ago(self):
        now = datetime.now(timezone('Asia/Seoul'))
        year = now.year
        month = now.month
        if month <= 2:
            month = 10 + month
            year -= 1
        else:
            month -= 2
        two_months_ago_time = datetime(year, month, 1, now.hour, now.minute)
        return two_months_ago_time.strftime('%Y%m%d%H%M')