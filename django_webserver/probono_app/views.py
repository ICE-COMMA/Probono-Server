from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
import requests
import xmltodict
from bson.json_util import loads, dumps
from datetime import datetime

from .models import SpecialWeather
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
# pdf 읽기
# import fitz # PyMuPDF 라이브러리 모듈
# import os
# from django.http import HttpResponse
#img 처리
# import pytesseract
# from PIL import Image
# import cv2 # img 내 테이블 처리(전처리)
# import numpy as np

# Mongo DB
from config import utils
from pymongo.errors import PyMongoError

# Session
from config.utils import SessionStore

# User
from .models import CustomUser
from .forms import SignUpForm



db_handle = utils.db_handle
get_collection = utils.get_collection_handle

def index(request):
    collection = get_collection(db_handle, 'special_weather')
    ret = list(collection.find({}))
    return render(request, 'index.html', { 'spw' : ret })

def my_page(request, id):
    try:
        current_user_id = request.session.get('ID', None)
        if not current_user_id:
            return HttpResponseForbidden("ACCESS DENIED")
        if request.method == 'GET':
            collection = get_collection(db_handle, 'User')
            ret = collection.find_one({'ID' : id})
            if not ret or str(ret['ID']) != str(current_user_id): 
                return HttpResponseForbidden("ACCESS DENIED")
            formatted_date = ret['date'].strftime('%Y.%m.%d')
            ret['date'] = formatted_date
            print(ret)
            return render(request, 'my_page.html', { 'info' : ret })
        elif request.method == 'POST':
            if str(id) != str(current_user_id): 
                return HttpResponseForbidden("ACCESS DENIED")
            collection = get_collection(db_handle, 'User')
            data = loads(request.body)
            print(data)
            update_result = collection.update_one({ 'ID' : id }, { '$set' : { data } })
            if update_result.matched_count == 0:
                return JsonResponse({ 'valid' : False, 'error' : 'Not found' })
            elif update_result.modified_count == 0: # Not modified
                return JsonResponse({ 'valid' : False, 'error' : 'Not modified' })
            return JsonResponse({ 'valid' : True })
    except PyMongoError:
        return JsonResponse({'valid': False, 'error': 'Database error'})

def transfer_info(request):
    return render(request, 'transfer_info.html')

def weather_info(request):
    return render(request, 'weather_info.html')

def dense_popul_info(request):
    return render(request, 'dense_popul_info.html')

def safety_info(request):
    return render(request, 'safety_info.html')

@require_POST
def login_view(request):
    users = get_collection(db_handle, 'User')
    user_id = request.POST.get('userid') # WARN : front's parameter name
    password = request.POST.get('password')
    user_info = users.find_one({'ID' : user_id})
    if user_info:
        if password == user_info['PW']:
            request.session['ID'] = user_id
            print(request.session.items())
            data = {
                    "success"      : True,
                    "redirect_url" : reverse('index') 
                    }
        else:
            data = { "success" : False }
    else:
        data = { "success" : False }
    status_code = 202
    return JsonResponse(data, status=status_code)

@require_POST
def sign_up(request):
    print(request.POST)
    form = SignUpForm(request.POST)
    if form.is_valid():
        print('GOOD')
        user_data = form.cleaned_data
        date_obj = form.cleaned_data['date']
        datetime_obj = datetime(date_obj.year, date_obj.month, date_obj.day)
        form.cleaned_data['date'] = datetime_obj
        user_data['custom'] = ''
        print(user_data)
        users = get_collection(db_handle, 'User')
        users.insert_one(form.cleaned_data)
        return redirect('index')
    print(form.errors)
    ret = { 'message' : 'error'}
    return JsonResponse(ret)

@require_POST
def id_check(request):
    users = get_collection(db_handle, 'User')
    data = loads(request.body)
    temp_id = data['check_id']
    temp = users.find_one({'ID' : temp_id})
    if not temp:
        data = { 'valid' : True } # REMIND : front have to know its response.
        status_code = 201
    else:
        status_code = 201
        data = { 'valid' : False } # REMIND : front have to know its response.
    return JsonResponse(data, status=status_code)

def logout_view(request):
    request.session.flush()
    return redirect('index')

@require_POST
def get_subway_elvtr(request):
    collection_elvtr = get_collection(db_handle, 'subway_elevator')
    search = request.POST.get('name')
    result = collection_elvtr.find({ 'sw_nm' : search })
    result = list(result)
    if not result:
        return JsonResponse({ 'message' : 'No results' })
    return JsonResponse({ 'result' : result})

def get_bus_no_to_route(request):
    
    return

def get_bus_route(request, bus_num):

    collection_bus = get_collection(db_handle, 'bus')
    bus_info = collection_bus.find_one({ 'bus_no' : bus_num })
    url = 'http://ws.bus.go.kr/api/rest/busRouteInfo/getStaionByRoute'
    key = '4cwiloFmPQxO3hXwmJy3jruoPPh6m8PQZqxBkWecSAgIIeRjq6UIdo0r7ZnmT4Rm4kVErRaD9jd1XU5CS7Chwg=='
    params = { 'ServiceKey' : key, 'busRouteId' : bus_info['route'], 'resultType' : 'json' }

    response = requests.get(url, params=params)
    print(response)
    data = response.json()
    item_list = data['msgBody']['itemList']
    # print(item_list)

    ret = []
    for target in item_list:
        data = {
            'name'  : target['stationNm'],
            'seq'   : target['seq'],
            'x'     : target['gpsX'],
            'y'     : target['gpsY']
        }
        ret.append(data)
    return JsonResponse({'station': ret})
    # print(ret[0])
    # return render(request, 'index.html', { 'station' : ret })

def get_safety_guard_house(request):
    
    return

def get_demo_today(request):
    
    chrome_options=webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=chrome_options)
    
    site_url = "https://www.smpa.go.kr/user/nd54882.do"
    driver.get(site_url)
    
    page_source=driver.page_source
    #soup = BeautifulSoup(page_source, 'html.parser')
    
    # 오늘 날짜
    current_date=datetime.now()
    year=current_date.strftime("%y")
    today=current_date.weekday()
    days=["월","화","수","목","금","토","일"]
    day=days[today]
    link_text="오늘의 집회 "
    date=year+current_date.strftime("%m%d") +" "+day # 원하는 날짜로 보려면 target_date로 받아야함
    xpath_expression = f"//a[contains(text(),'{link_text}{date}')]"
    element = driver.find_element(By.XPATH, xpath_expression)
    driver.execute_script("arguments[0].scrollIntoView();", element)
    
    # 새 페이지로 이동
    element.click()
    current_url=driver.current_url
    
    wait = WebDriverWait(driver, 10)
    # 이미지 요소의 XPath로 이미지를 찾고, src 속성을 가져옴
    image_element = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='bcontent']//img")))
    image_url = image_element.get_attribute("src")    
    
    # WebDriver 종료
    driver.quit()
    
    # 프론트에 던져줄 정보
    context = {
        'link_text': link_text,
        'link_url': current_url,
        'img_url': image_url, # 이걸 받으면 됨
    }
        
    return render(request, 'demo.html', context)