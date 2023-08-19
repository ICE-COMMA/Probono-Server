from django.db import models
import requests

# DB
from bson.objectid import ObjectId
from bson.json_util import loads, dumps

# Special Weather
from datetime import datetime
from itertools import groupby

class CustomUser():

    # user_id
    ID = models.CharField(max_length=100, unique=True)

    PW = models.CharField(max_length=100)
    # user name
    name = models.CharField(max_length=100)
    # sex
    gender = models.CharField(max_length=1)
    # birth
    date = models.DateField()
    # disability
    impaired = models.CharField(max_length=50)
    # custom
    custom = models.CharField(max_length=10)
    
    def __str__(self):
        return self.ID
    
class Bus():
    
    #object_id
    obj_id=models.CharField(max_length=100)
    #bus number
    bus_num=models.CharField(max_length=100)
    #station
    station=models.CharField(max_length=100)
    
    def __str__(self):
        return self.obj_id
    
class Bus_Station():
    
    #object_id
    obj_id=models.CharField(max_length=100)
    #bus station name
    stat_name=models.CharField(max_length=100)
    #latitude
    x=models.CharField(max_length=100)
    #longitude
    y=models.CharField(max_length=100)
    
    def __str__(self):
        return self.stat_name
    
class Subway_Station():
    
    #object_id
    obj_id=models.CharField(max_length=100)
    #bus station name
    stat_name=models.CharField(max_length=100)
    #latitude
    x=models.CharField(max_length=20)
    #longitude
    y=models.CharField(max_length=20)
    #elevator_x
    elevator_x=models.CharField(max_length=20)
    #elevator_y
    elevator_y=models.CharField(max_length=20)
    
    def __str__(self):
        return self.stat_name
    
    
class Police_Station():
    
    #object_id
    obj_id=models.CharField(max_length=100)
    #bus station name
    stat_name=models.CharField(max_length=100)
    #latitude
    x=models.CharField(max_length=100)
    #longitude
    y=models.CharField(max_length=100)
    
    def __str__(self):
        return self.stat_name
    
class Population_Density_Info():
    
    #object_id
    obj_id=models.CharField(max_length=100)
    #date
    date=models.CharField(max_length=100)
    #time
    time=models.CharField(max_length=100)
    #bus station name
    amount=models.CharField(max_length=100)
    #latitude
    x=models.CharField(max_length=100)
    #longitude
    y=models.CharField(max_length=100)
    
    def __str__(self):
        return self.obj_id

class Safety_Guard_House():
    
    #object_id
    obj_id=models.CharField(max_length=100)
    #name
    name=models.CharField(max_length=100)
    #latitude
    x=models.CharField(max_length=100)
    #longitude
    y=models.CharField(max_length=100)
    
    def __str__(self):
        return self.obj_id
    
class demo():
    
    #object_id
    obj_id=models.CharField(max_length=100)
    #name
    name=models.CharField(max_length=100)
    #location
    location=models.CharField(max_length=100)
    #date
    date=models.CharField(max_length=100)
    #time
    time=models.CharField(max_length=100)
    #amount
    amount=models.CharField(max_length=100)
    
    def __str__(self):
        return self.obj_id

class SpecialWeather():

    tmfc1_value = None

    def __init__(self):
        self.target_reg = [
            ['L1100100', '서울동남권'],
            ['L1100200', '서울동북권'],
            ['L1100300', '서울서남권'],
            ['L1100400', '서울서북권']
        ]
        self.wrn = {
            'W': '강풍', 'R': '호우', 'C': '한파',
            'D': '건조', 'O': '해일', 'N': '지진해일',
            'V': '풍랑', 'T': '태풍', 'S': '대설',
            'Y': '황사', 'H': '폭염'
        }
        self.lvl = {'1': '예비', '2': '주의보', '3': '경보'}
        self.key = 'm4y76-4OTnaMu-vuDg525w'

    # main method
    def init_special_weather(self, special_weathers):
        special_weathers.delete_many({})
        to_insert = []
        for target in self.target_reg:
            content_str = self.init_fetch_data(target, self.key)
            all_data = self.parse_data(content_str, target)
            all_data.sort(key=lambda x: (x['WRN'], x['TM_EF']))
            grouped_data = {key: list(group) for key, group in groupby(all_data, key=lambda x: x['WRN'])}
            to_insert.extend(self.process_grouped_data(grouped_data, target))
        special_weathers.insert_many(to_insert)

    # main method
    def update_special_weather(self, special_weathers):
        new_data = []
        for target in self.target_reg:
            content_str = self.update_fetch_data(target, self.key)
            all_data = self.parse_data(content_str, target)
            all_data.sort(key=lambda x: (x['WRN'], x['TM_EF']))
            grouped_data = {key: list(group) for key, group in groupby(all_data, key=lambda x: x['WRN'])}
            new_data.extend(self.process_grouped_data(grouped_data, target))

        for target in new_data:
            target_db = special_weathers.find_one(target['WRN'])
            if not target_db:
                special_weathers.delete_one(target_db)
                if target['CMD'] != '3':
                    special_weathers.insert_one(target)

    def init_fetch_data(self, target, key):
        SpecialWeather.tmfc1_value = self.two_months_ago()
        url = 'https://apihub.kma.go.kr/api/typ01/url/wrn_met_data.php'
        params = {'wrn': 'A', 'reg': target[0], 'tmfc1': SpecialWeather.tmfc1_value, 'disp': '0', 'authKey': key}
        SpecialWeather.tmfc1_value = datetime.now().strftime('%Y%m%d%H%M')
        response = requests.get(url, params=params)
        return response.content.decode('utf-8')

    def update_fetch_data(self, target, key):
        url = 'https://apihub.kma.go.kr/api/typ01/url/wrn_met_data.php'
        params = {'wrn': 'A', 'reg': target[0], 'tmfc1': SpecialWeather.tmfc1_value, 'disp': '0', 'authKey': key}
        SpecialWeather.tmfc1_value = datetime.now().strftime('%Y%m%d%H%M')
        response = requests.get(url, params=params)
        return response.content.decode('utf-8')

    def parse_data(self, content_str, target):
        content_str = content_str.replace("#START7777", "").replace("#7777END", "").strip()
        lines = content_str.split('\n')
        all_data = []
        for line in lines:
            if line.startswith("#"):
                continue
            fields = line.split(',')
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
        now = datetime.now()
        year = now.year
        month = now.month
        if month <= 2:
            month = 10 + month
            year -= 1
        else:
            month -= 2
        two_months_ago_time = datetime(year, month, now.day, now.hour, now.minute)
        return two_months_ago_time.strftime('%Y%m%d%H%M')