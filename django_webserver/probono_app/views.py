from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.http import HttpResponse, JsonResponse
import requests
import xmltodict
from bson.json_util import loads, dumps
from datetime import datetime
from itertools import groupby

from .models import SpecialWeather
# crawling`
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
# 구글링해서 찾은것, 지울수도
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
#요소 클릭 위해
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
#img_url
from urllib.parse import urljoin

# Mongo DB
from config import utils

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

def my_page(request):
    return render(request, 'my_page.html')

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
    print(request.POST)
    print(user_id, password)
    user_info = users.find_one({'ID' : user_id})
    print(user_info)
    if user_info:
        if password == user_info['PW']:
            request.session['ID'] = user_id
            print(request.session['ID'])
            data = {
                    "success"      : True,
                    "redirect_url" : reverse('index') 
                    }
        else:
            data = { "success" : False }
    else:
        data = { "success" : False }
    status_code = 201
    print(data)
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
    temp = users.find_one({'id' : temp_id})
    if not temp:
        data = { 'valid' : True } # REMIND : front have to know its response.
        status_code = 201
    else:
        status_code = 201
        data = { 'valid' : False } # REMIND : front have to know its response.
    return JsonResponse(data, status=status_code)

def logout_view(request):
    del request.session['ID']
    print(request.session['ID'])
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

def get_bus_route(request):

    # collection_bus = get_collection(db_handle, 'bus')
    # num = request.POST.get('bus_num')
    # route = collection_bus.find_one(num)
    route = 100100001
    url = 'http://ws.bus.go.kr/api/rest/busRouteInfo/getStaionByRoute'
    params = { 'ServiceKey' : '4cwiloFmPQxO3hXwmJy3jruoPPh6m8PQZqxBkWecSAgIIeRjq6UIdo0r7ZnmT4Rm4kVErRaD9jd1XU5CS7Chwg==', 'busRouteId' : str(route), 'resultType' : 'xml' }

    response = requests.get(url, params=params)
    print(response)
    print(response.content)
    data_dict = xmltodict.parse(response.content)
    print(data_dict)
    data = data_dict.get('busRoute')
    print(data)

    return render(request, 'index.html')

def get_safety_guard_house(request):
    
    return

def crawl_notice(request, target_date):
    
    chrome_options=webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    
    site_url = "https://www.smpa.go.kr/user/nd54882.do"
    driver.get(site_url)
    
    page_source=driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    
    # 원하는 정보 추출
    target_element = None
    for td_element in soup.find_all('td', class_='subject'):
        date_column = td_element.get_text().strip()
        if date_column == target_date:
            target_element = td_element
            break
       
    link_text="오늘의 집회 "
    date="230821 월"
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

    # link_text=None
    # link_url=None
    # img_url=None
    # if target_element:
    #     link = target_element.find('a')
    #     link_text = link.get_text()
    #     link_url = link['href']
        
    
    
    # 여기서 javascript함수로 되어있는 동적 정보 url로 접근해야함    
    dynamic_content=soup.find('div',class_='reply-content')
    if dynamic_content:
        print('find')
        img_url=dynamic_content['src']
    # WebDriver 종료
    driver.quit()
    
    context = {
        'link_text': link_text,
        'link_url': current_url,
        'img_url': image_url,
    }
        
    return render(request, 'crawl_result.html', context)