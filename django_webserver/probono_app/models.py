from django.db import models
import requests

# DB
from bson.objectid import ObjectId
from bson.json_util import loads, dumps

# User
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Special Weather
from datetime import datetime
from itertools import groupby

# 이거 완전 쓸모 없어 형석아 지우자
class CustomUserManager(BaseUserManager):

    def create_user(self, user_id, name, password, sex, birth, disability, custom):

        if not user_id:
            raise ValueError('아이디는 필수입니다.')
        if not name:
            raise ValueError('이름은 필수입니다.')
        if not password:
            raise ValueError('비밀번호는 필수입니다.')
        if sex == 0:
            raise ValueError('성별은 필수입니다.')
        if birth == 0:
            raise ValueError('생년월일은 필수입니다.')
        if disability == 0:
            raise ValueError('장애여부는 필수입니다.')

        user = self.model(user_id = user_id, sex = sex, birth = birth, disability = disability, custom = custom)
        user.set_password(password)
        user.save(using=self._db)
        return user

    # 보류
    def create_superuser(self, user_id, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser는 is_staff=True여야 합니다.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser는 is_superuser=True여야 합니다.')

        return self.create_user(user_id, password, **extra_fields)

class CustomUser(AbstractBaseUser):

    # user_id
    user_id = models.CharField(max_length=100, unique=True)
    # user name
    name = models.CharField(max_length=100)
    # sex
    sex = models.CharField(max_length=1)
    # birth
    birth = models.DateField()
    # disability
    disability = models.CharField(max_length=10)
    # custom
    custom = models.CharField(max_length=10)

    is_staff = models.BooleanField(default=False)
    
    objects = CustomUserManager()

    USERNAME_FIELD = 'user_id'

    # 보류
    REQUIRED_FIELDS = ['user_id']

    # 보류
    def __str__(self):
        return self.user_id
    
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

class SpecialWeather:
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
            content_str = self.fetch_data(target, self.key)
            all_data = self.parse_data(content_str, target)
            all_data.sort(key=lambda x: (x['WRN'], x['TM_EF']))
            grouped_data = {key: list(group) for key, group in groupby(all_data, key=lambda x: x['WRN'])}
            to_insert.extend(self.process_grouped_data(grouped_data, target))
        special_weathers.insert_many(to_insert)

    # main method
    def update_special_weather(self, special_weathers):

        
        
        
        return

    def fetch_data(self, target, key):
        url = 'https://apihub.kma.go.kr/api/typ01/url/wrn_met_data.php'
        params = {'wrn': 'A', 'reg': target[0], 'tmfc1': self.two_months_ago(), 'disp': '0', 'authKey': key}
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

    def two_months_ago():
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