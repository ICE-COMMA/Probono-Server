import requests
from celery import shared_task
from config import settings, utils
from .models import SpecialWeather

'''
서버 구동 후, 반드시 터미널 창 두개 열어서 실행해야 함.

celery -A your_project worker -l info
celery -A your_project beat -l info
'''

db_handle = utils.db_handle
get_collection = utils.get_collection_handle

@shared_task
def get_subway_elvtr_task():
    base_url = 'http://openapi.seoul.go.kr:8088/4f6a5a74796c696d3534425a686562/json/tbTraficElvtr'
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

    # save to Mongo DB
    collection_elevtr = get_collection(db_handle, 'subway_elevator')
    collection_elevtr.delete_many({})
    for data in all_data:
        sw_nm = data.get('SW_NM', '')
        node_wkt = data.get('NODE_WKT', '')
        coordinates = node_wkt.replace("POINT(", "").replace(")", "").split()
        x = coordinates[0]
        y = coordinates[1]
        subway_elevator = {
            'sw_nm' : sw_nm,
            'x'     : x,
            'y'     : y
        }
        collection_elevtr.insert_one(subway_elevator)
    return

@shared_task
def get_bus_no_to_route():
    base_url = 'http://openapi.seoul.go.kr:8088/57636d66616c696d3536664b555850/json/busRoute'
    start_index = 1
    end_index = 100

    all_data = []
    while True:
        url = f"{base_url}/{start_index}/{end_index}/"
        response = requests.get(url)
        data = response.json()
        if 'busRoute' in data and 'row' in data['busRoute']:
            all_data.extend(data['busRoute']['row'])
        start_index += 100
        end_index += 100
        if len(data['busRoute']['row']) < 100:
            break

    # save to Mongo DB
    collection_bus = get_collection(db_handle, 'bus')
    collection_bus.delete_many({})
    for data in all_data:
        bus_no = data.get('ROUTE', '')
        route = data.get('ROUTE_ID', '')
        no_to_route = {
            'bus_no'    : bus_no,
            'route'     : route
        }
        collection_bus.insert_one(no_to_route)
    return

@shared_task
def get_safety_guard_house():
    base_url="http://api.data.go.kr/openapi/tn_pubr_public_female_safety_prtchouse_api"
    start_index=1
    end_index=100
    
    collection_guard = get_collection(db_handle, 'safety_guard_house')
    collection_guard.delete_many({})
    while True:
        params={'serviceKey' : 'z3tbVitFT7XffZ43RQ9sMyE0ALiv+EtqOysMUKPdg9E5zTIL3lNVHqGCOS9vPqq73zYw6OhwHiskVZj4MYCJ0w==',
                'pageNo' : start_index,
                'numOfRows' : end_index,
                'type' : 'json' }
        response = requests.get(base_url,params=params)
        data = response.json() 

        if 'response' in data and 'body' in data['response'] and 'items' in data['response']['body']:
            items = data['response']['body']['items']
            for target in items:
                if target['ctprvnNm']=='서울특별시':
                    name = target.get('storNm', '')
                    x = target.get('latitude', '')
                    y = target.get('longitude', '')
                    safety_guard_house = {
                        'name'    : name,
                        'x'     : x,
                        'y'     : y
                    }
                    collection_guard.insert_one(safety_guard_house)
            if len(items) < 100:
                break
        else:
            break
        start_index += 1
    return

@shared_task
def update_special_weather_task():
    special_weather = SpecialWeather()
    collection = get_collection(db_handle, 'special_weather')
    special_weather.update_special_weather(collection)
    return

import olefile
import zlib
import struct
import os
import re
from datetime import datetime
# crawling
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
#요소 클릭 위해
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

@shared_task
def get_hwp_txt():
    chrome_options=webdriver.ChromeOptions()
    # chrome 창 안보이게
    # chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=chrome_options)
    wait=WebDriverWait(driver,10) # wait time define
    download_path='C:\\Users\\limhs\\Downloads'
    
    site_url = "https://www.smpa.go.kr/user/nd54882.do"
    driver.get(site_url)
    
    page_source=driver.page_source

    # 오늘 날짜
    current_date=datetime.now()
    year=current_date.strftime("%y")
    today=current_date.weekday()
    days=["월","화","수","목","금","토","일"]
    day=days[today]
    link_text="오늘의 집회"
    date=year+current_date.strftime("%m%d") # 원하는 날짜로 보려면 target_date로 받아야함
    blank=" "
    xpath_expression = f"//a[contains(text(),'{link_text}{blank}{date}{blank}{day}')]"
    element = driver.find_element(By.XPATH, xpath_expression)
    driver.execute_script("arguments[0].scrollIntoView();", element) #해당 요소로 스크롤 이동

    # 새 페이지로 이동
    element.click()

    target_filename=date+"("+day+")"+blank+"인터넷집회.hwp"
    xpath_expression=f"//a[contains(text(), '{target_filename}')]"
    #links = driver.find_element(By.XPATH, xpath_expression)
    links = driver.find_elements(By.XPATH, f"//a[@class='doc_link']")
    download_link = None
    text=""

    for link in links:
        if target_filename in link.text:
            text="find"
            download_link = link
            break

    # 링크가 찾아지면 클릭해서 다운로드
    if download_link:
        driver.execute_script("arguments[0].scrollIntoView();", download_link) #해당 요소로 스크롤 이동
        download_link.click()
        # 해당 경로에 해당 파일이 있을 때까지 대기
        wait.until(lambda driver: target_filename in os.listdir(download_path))

    # WebDriver 종료
    driver.quit()

    file_path="C:/Users/limhs/Downloads/"+target_filename
    new_filename=date+'demo.hwp'
    new_file_path=os.path.join(os.path.dirname(file_path),new_filename)
    #os.rename(file_path,new_file_path)
    
    f=olefile.OleFileIO(new_file_path)
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
    
    collenction_demo=get_collection(db_handle,'demo')
    collenction_demo.delete_many({})
    
    
    date = re.search(r'\d{4}\. \d{2}\. \d{2}',text)
    cnt=len(re.findall(r'(\d{2}:\d{2})[∼~](\d{2}:\d{2})',text))
    text = text.replace('\r','').replace('\n','')
    for i in range(cnt+1):
        match = re.search(r'(\d{2}:\d{2})[∼~](\d{2}:\d{2})',text)
        if match:
            time=text[match.start():match.end()]
            text=text[match.end():]
            print(time)
        
        match = re.search(r'<[^>]+>',text)
        if match:
            place=text[:match.end()]
            text=text[match.end():]
            print(place)
        
        match = re.search(r'\d{1,3}(,\d{3})*',text)
        if match:
            amount=text[match.start():match.end()]
            text=text[match.end():]
            print(amount)
            
        demo={
            'location':place,
            'date':date,
            'time': time,
            'amount':amount
        }
        collenction_demo.insert_one(demo)
        i+=1

    return