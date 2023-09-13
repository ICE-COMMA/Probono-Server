from django.db import models
import requests
from pytz import timezone

# DB
from bson.objectid import ObjectId
from bson.json_util import loads, dumps

# Special Weather
from datetime import datetime
from itertools import groupby


import os
import openpyxl

# Population_real_time
from concurrent.futures import ThreadPoolExecutor, as_completed

# DemoScraper
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os
import olefile
import re
import zlib
import struct

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

    # object_id
    obj_id = models.CharField(max_length=100)
    # bus number
    bus_num = models.CharField(max_length=100)
    # station
    station = models.CharField(max_length=100)

    def __str__(self):
        return self.obj_id

class Bus_Station():

    # object_id
    obj_id = models.CharField(max_length=100)
    # bus station name
    stat_name = models.CharField(max_length=100)
    # latitude
    x = models.CharField(max_length=100)
    # longitude
    y = models.CharField(max_length=100)

    def __str__(self):
        return self.stat_name

class Subway_Station():

    # object_id
    obj_id = models.CharField(max_length=100)
    # bus station name
    stat_name = models.CharField(max_length=100)
    # latitude
    x = models.CharField(max_length=20)
    # longitude
    y = models.CharField(max_length=20)
    # elevator_x
    elevator_x = models.CharField(max_length=20)
    # elevator_y
    elevator_y = models.CharField(max_length=20)

    def __str__(self):
        return self.stat_name

class Police_Station():

    # object_id
    obj_id = models.CharField(max_length=100)
    # bus station name
    stat_name = models.CharField(max_length=100)
    # latitude
    x = models.CharField(max_length=100)
    # longitude
    y = models.CharField(max_length=100)

    def __str__(self):
        return self.stat_name

class Population_Density_Info():

    # object_id
    obj_id = models.CharField(max_length=100)
    # date
    date = models.CharField(max_length=100)
    # time
    time = models.CharField(max_length=100)
    # bus station name
    amount = models.CharField(max_length=100)
    # latitude
    x = models.CharField(max_length=100)
    # longitude
    y = models.CharField(max_length=100)

    def __str__(self):
        return self.obj_id

class Safety_Guard_House():

    # object_id
    obj_id = models.CharField(max_length=100)
    # name
    name = models.CharField(max_length=100)
    # latitude
    x = models.CharField(max_length=100)
    # longitude
    y = models.CharField(max_length=100)

    def __str__(self):
        return self.obj_id

class data():

    # object_id
    obj_id = models.CharField(max_length=100)
    # name
    name = models.CharField(max_length=100)
    # location
    location = models.CharField(max_length=100)
    # date
    date = models.CharField(max_length=100)
    # time
    time = models.CharField(max_length=100)
    # amount
    amount = models.CharField(max_length=100)

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
            grouped_data = {key: list(group) for key, group in groupby(
                all_data, key=lambda x: x['WRN'])}
            to_insert.extend(self.process_grouped_data(grouped_data, target))
        print(to_insert)
        if to_insert:
            special_weathers.insert_many(to_insert)

    # main method
    def update_special_weather(self, special_weathers):
        new_data = []
        for target in self.target_reg:
            content_str = self.update_fetch_data(target, self.key)
            all_data = self.parse_data(content_str, target)
            all_data.sort(key=lambda x: (x['WRN'], x['TM_EF']))
            grouped_data = {key: list(group) for key, group in groupby(
                all_data, key=lambda x: x['WRN'])}
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
        params = {
            'wrn': 'A', 'reg': target[0], 'tmfc1': SpecialWeather.tmfc1_value, 'disp': '0', 'authKey': key}
        SpecialWeather.tmfc1_value = datetime.now().strftime('%Y%m%d%H%M')
        response = requests.get(url, params=params)
        return response.content.decode('utf-8')

    def update_fetch_data(self, target, key):
        url = 'https://apihub.kma.go.kr/api/typ01/url/wrn_met_data.php'
        params = {
            'wrn': 'A', 'reg': target[0], 'tmfc1': SpecialWeather.tmfc1_value, 'disp': '0', 'authKey': key}
        SpecialWeather.tmfc1_value = datetime.now().strftime('%Y%m%d%H%M')
        response = requests.get(url, params=params)
        return response.content.decode('utf-8')

    def parse_data(self, content_str, target):
        content_str = content_str.replace(
            "#START7777", "").replace("#7777END", "").strip()
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
        now = datetime.now(timezone('Asia/Seoul'))
        year = now.year
        month = now.month
        if month <= 2:
            month = 10 + month
            year -= 1
        else:
            month -= 2
        print(now)
        two_months_ago_time = datetime(year, month, 1, now.hour, now.minute)
        return two_months_ago_time.strftime('%Y%m%d%H%M')

class Bus_info():

    def __init__(self):
        self.base_url = 'http://ws.bus.go.kr/api/rest/buspos/getBusPosByRtid'
        self.key = '4cwiloFmPQxO3hXwmJy3jruoPPh6m8PQZqxBkWecSAgIIeRjq6UIdo0r7ZnmT4Rm4kVErRaD9jd1XU5CS7Chwg=='
        self.bus_type = { '0' : False, '1' : True, '2' : False }
        self.bool = { '0' : False, '1' : True }

    def get_bus_pos(self, route_id):
        params = {'serviceKey' : self.key, 'busRouteId' : route_id, 'resultType' : 'json'}
        data = self.fetch_data(params)
        data = data['bus_pos']['msgBody']['itemList']
        ret = {
            'is_low'            : data['busType'],
            'is_bus_stopped'    : data['stopFlag'],
            'is_full'           : data['isFullFlag'],
            'is_last'           : data['islastyn'],
            'congestion'        : data['congetion'],
            'next_station_id'   : data['nextStId'],
            'next_time'         : data['nextStTm']
        }
        print(ret)
        return ret

    def fetch_data(self, params):
        response = requests.get(self.base_url, params=params)
        return response.json()

class Population_real_time():

    def __init__(self):
        self.base_url = 'http://openapi.seoul.go.kr:8088/68666f624d6c696d373249736e7649/json/citydata_ppltn'

    def init_population_info(self, region_info):
        region_info.delete_many({})
        to_insert = self.get_xl_file_info()
        region_info.insert_many(to_insert)

    def get_xl_file_info(self):
        file_path = os.path.join(os.path.dirname(
            __file__), 'files', 'population_region_info.xlsx')
        xl_file = openpyxl.load_workbook(file_path)
        xl_sheet = xl_file.active

        data_list = []
        for row_idx, row in enumerate(xl_sheet.iter_rows(values_only=True), start=1):
            if row_idx == 1:
                continue
            category = row[0]
            no = row[1]
            area_cd = row[2]
            area_nm = row[3]
            data_list.append({
                'CATEGORY': category,
                'NO': no,
                'AREA_CD': area_cd,
                'AREA_NM': area_nm,
            })
        xl_file.close()
        return data_list

    def fetch_data(self, url):
        response = requests.get(url)
        return response.json()

    # def get_real_time_popul(self, region_info):
    #     start_index = 1
    #     end_index = 5

    #     ret = []
    #     for target in region_info:
    #         code_target = target['AREA_CD']
    #         print(code_target)
    #         url = f"{self.base_url}/{start_index}/{end_index}/{code_target}"
    #         response = requests.get(url)
    #         temp = response.json()
    #         temp = temp['SeoulRtd.citydata_ppltn'][0]
    #         print(temp)
    #         data = {
    #             'area_name'         : temp['AREA_NM'],
    #             'area_code'         : temp['AREA_CD'],
    #             'area_congest'      : temp['AREA_CONGEST_LVL'],
    #             'message'           : temp['AREA_CONGEST_MSG'],
    #             'area_popul_min'    : temp['AREA_PPLTN_MIN'],
    #             'area_popul_max'    : temp['AREA_PPLTN_MAX'],
    #             'area_update_time'  : temp['PPLTN_TIME']
    #         }
    #         ret.append(data)
    #     return ret

    def get_real_time_popul(self, region_info):
        start_index = 1
        end_index = 5

        ret = []
        # Multithreading for optimization
        with ThreadPoolExecutor() as executor:
            future_to_url = {executor.submit(
                self.fetch_data, f"{self.base_url}/{start_index}/{end_index}/{target['AREA_CD']}"): target for target in region_info}
            for future in as_completed(future_to_url):
                target = future_to_url[future]
                try:
                    temp = future.result()['SeoulRtd.citydata_ppltn'][0]
                    area_popul_average = round(
                        (int(temp['AREA_PPLTN_MIN']) + int(temp['AREA_PPLTN_MAX'])) / 2)
                    data = {
                        'area_name': temp['AREA_NM'],
                        'area_code': temp['AREA_CD'],
                        'area_congest': temp['AREA_CONGEST_LVL'],
                        'message': temp['AREA_CONGEST_MSG'],
                        'area_popul_min': temp['AREA_PPLTN_MIN'],
                        'area_popul_max': temp['AREA_PPLTN_MAX'],
                        'area_popul_avg': area_popul_average,
                        'area_update_time': temp['PPLTN_TIME']
                    }
                    ret.append(data)
                except Exception as exc:
                    print(f'{target["AREA_CD"]} generated an exception: {exc}')

        ret = sorted(ret, key=lambda x: x['area_popul_avg'], reverse=True)
        return ret

class Population_AI_model():

    def __init__(self):
        self.base_url = 'http://openapi.seoul.go.kr:8088/4b4c477a766c696d39314965686a66/json/SPOP_LOCAL_RESD_DONG/1/5/20230907/ '
        self.region_code = ['11500540', '11380625', '11380690', '11740685']

    def init_population_AI(self):
        return

    def update_population_AI(self):

        ret = []
        for target in self.region_code:
            data = self.fetch_data(f"{self.base_url}/{target}")
            ret.append(data)
        return ret

    def fetch_data(self, url):
        response = requests.get(url)
        return response.json()

class DemoScraper:

    def __init__(self):
        self.chrome_options = webdriver.ChromeOptions()
        self.download_path = '/Users/choijeongheum/Downloads/'
        self.site_url = "https://www.smpa.go.kr/user/nd54882.do"

    def start_driver(self):
        # self.chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(service=Service(
            ChromeDriverManager().install()), options=self.chrome_options)
        self.wait = WebDriverWait(self.driver, 10)

    def navigate_to_site(self):
        self.driver.get(self.site_url)

    def get_date_info(self):
        current_date = datetime.now(timezone('Asia/Seoul'))
        print('NOW!!!!!!!!!!!', current_date)
        year = current_date.strftime("%y")
        today = current_date.weekday()
        days = ["월", "화", "수", "목", "금", "토", "일"]
        day = days[today]
        self.date = year + current_date.strftime("%m%d")
        self.day = day

    def click_on_today_demo(self):
        link_text = "오늘의 집회"
        blank = " "
        xpath_expression = f"//a[contains(text(),'{link_text}{blank}{self.date}{blank}{self.day}')]"
        element = self.driver.find_element(By.XPATH, xpath_expression)
        self.driver.execute_script("arguments[0].scrollIntoView();", element)
        element.click()

    def download_hwp(self):
        file_name_text = "인터넷집회"
        target_filename = self.date + \
            "(" + self.day + ")" + " " + file_name_text + ".hwp"
        xpath_expression = f"//a[contains(text(), '{target_filename}')]"
        links = self.driver.find_elements(By.XPATH, f"//a[@class='doc_link']")
        download_link = None
        for link in links:
            if target_filename in link.text:
                download_link = link
                break
        if download_link:
            self.driver.execute_script(
                "arguments[0].scrollIntoView();", download_link)
            download_link.click()
            self.wait.until(
                lambda driver: target_filename in os.listdir(self.download_path))

    def process_hwp_file(self):

        # 파일명에서 한글 없애기(파일경로 수정 요망)
        file_path = "/Users/choijeongheum/Downloads/" + self.date + \
            "(" + self.day + ")" + " " + "인터넷집회.hwp"
        new_filename = self.date + 'data.hwp'
        new_file_path = os.path.join(os.path.dirname(file_path), new_filename)
        os.rename(file_path, new_file_path)

        # HWP 파일 처리
        with olefile.OleFileIO(new_file_path) as f:
            dirs = f.listdir()

            # HWP 파일 검증
            if ["FileHeader"] not in dirs or \
                    ["\x05HwpSummaryInformation"] not in dirs:
                raise Exception("Not Valid HWP.")

            # 문서 포맷 압축 여부 확인
            header = f.openstream("FileHeader")
            header_data = header.read()
            is_compressed = (header_data[36] & 1) == 1

            # Body Sections 불러오기
            nums = []
            for d in dirs:
                if d[0] == "BodyText":
                    nums.append(int(d[1][len("Section"):]))
            sections = ["BodyText/Section"+str(x) for x in sorted(nums)]

            # 전체 text 추출
            text = ""
            for section in sections:

                bodytext = f.openstream(section)
                data = bodytext.read()
                if is_compressed:
                    unpacked_data = zlib.decompress(data, -15)
                else:
                    unpacked_data = data

                # 각 Section 내 text 추출
                section_text = ""
                i = 0
                size = len(unpacked_data)
                while i < size:
                    header = struct.unpack_from("<I", unpacked_data, i)[0]
                    rec_type = header & 0x3ff
                    rec_len = (header >> 20) & 0xfff

                    if rec_type in [67]:
                        rec_data = unpacked_data[i+4:i+4+rec_len]
                        section_text += rec_data.decode('utf-16')
                        section_text += "\n"

                    i += 4 + rec_len

                text += section_text
                text += "\n"

            to_insert = []
            date = re.search(r'\d{4}\. \d{2}\. \d{2}', text)
            cnt = len(re.findall(r'(\d{2}:\d{2})[∼~](\d{2}:\d{2})', text))
            text = text.replace('\r', '').replace('\n', '')
            for i in range(cnt+1):
                match = re.search(r'(\d{2}:\d{2})[∼~](\d{2}:\d{2})', text)
                if match:
                    time = text[match.start():match.end()]
                    text = text[match.end():]
                    # print(time)

                i = 0
                while (1):
                    if text[i].isalnum() and not 0x4E00 <= ord(text[i]) <= 0x9FFF:
                        break
                    i += 1

                match = re.search(r'<[^>]+>', text)
                if match:
                    place = text[i:match.end()]
                    text = text[match.end():]
                    # print(place)

                match = re.search(r'\d{1,3}(,\d{3})*', text)
                if match:
                    amount = text[match.start():match.end()]
                    text = text[match.end():]
                    # print(amount)

                result = {
                    'location': place,
                    'date': date,
                    'time': time,
                    'amount': amount
                }
                to_insert.append(result)
                i += 1

        return to_insert

    # MODIFY LATER
    def update_demo(self, collection):
        collection.delete_many({})
        new_data = []
        new_data.extend(self.process_hwp_file())
        for idx, target in enumerate(new_data):
            new_data[idx]['date'] = target['date'].group()

        print(new_data)
        collection.insert_many(new_data)

    def close_driver(self):
        self.driver.quit()

    def get_demo(self, collection):
        self.start_driver()
        self.navigate_to_site()
        self.get_date_info()
        self.click_on_today_demo()
        self.download_hwp()
        self.update_demo(collection)
        self.close_driver()
        return