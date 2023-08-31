from django.db import models
import requests

# DB
from bson.objectid import ObjectId
from bson.json_util import loads, dumps

# Special Weather
from datetime import datetime
from itertools import groupby

import pandas as pd
import os
import openpyxl
# from openpyxl.drawing.image import Image
from io import BytesIO
import xlwings as xw
from PIL import ImageGrab, Image

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
        now = datetime.now()
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


class Population_real_time():

    def get_xl_file_info(self):
        file_path = os.path.join(os.path.dirname(
            __file__), 'files', 'population_region_info.xlsx')
        xl_file = openpyxl.load_workbook(file_path)
        xl_sheet = xl_file.active

        data_list = []
        # image_data_dict = {}
        # for image in xl_sheet._images:
        #     col, row = image.anchor.tl.col, image.anchor.tl.row  # 이미지가 위치한 셀의 좌표
        #     image_data_dict[(col, row)] = image.image._data
        # print(image_data_dict)

        for row_idx, row in enumerate(xl_sheet.iter_rows(values_only=True), start=1):
            if row_idx == 1:
                continue

            category = row[0]
            no = row[1]
            area_cd = row[2]
            area_nm = row[3]

            photo_data = None

            data_list.append({
                'CATEGORY': category,
                'NO': no,
                'AREA_CD': area_cd,
                'AREA_NM': area_nm,
                'PHOTO': photo_data
            })

        for item in data_list:
            print(item)
        xl_file.close()

        app = xw.App(visible=False)
        wb = app.books.open(file_path)
        sheet = wb.sheets['region_info']

        # temp_file = "temp_image.jpg"
        image = sheet.pictures
        print(image)
        image.api.Copy()

        img = ImageGrab.grabclipboard()

        temp_file = "temp_image.jpg"
        img.save(temp_file)
        # image.api.Copy()
        # print(xl_sheet.pictures[0])
        # xl_sheet.pictures[0].api.Copy()
        # sheet.pictures[0].api.Copy()
        # img = ImageGrab.grabclipboard()
        # image.save(temp_file)

        # print(img)
        # image_bytes = image.image
        # print(image_bytes)
        # sheet.pictures[0].api.Copy()
        # img = ImageGrab.grabclipboard()
        # print(image)

        wb.close()
        app.quit()


class DemoScraper:

    def __init__(self):
        self.chrome_options = webdriver.ChromeOptions()
        self.download_path = 'C:\\Users\\admin\\Downloads'
        self.site_url = "https://www.smpa.go.kr/user/nd54882.do"

    def start_driver(self):
        # self.chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(service=Service(
            ChromeDriverManager().install()), options=self.chrome_options)
        self.wait = WebDriverWait(self.driver, 10)

    def navigate_to_site(self):
        self.driver.get(self.site_url)

    def get_date_info(self):
        current_date = datetime.now()
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
        file_path = "C:/Users/admin/Downloads/" + self.date + \
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

                match = re.search(r'<[^>]+>', text)
                if match:
                    place = text[:match.end()]
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

    def update_demo(self, demos):

        new_data = []
        new_data.extend(self.process_hwp_file())
        for target in new_data:
            demos.insert_one(target)
            print(target)

    def close_driver(self):
        self.driver.quit()

    def get_demo(self, demos):
        self.start_driver()
        self.navigate_to_site()
        self.get_date_info()
        self.click_on_today_demo()
        self.download_hwp()
        self.update_demo(demos)
        self.close_driver()
        return
