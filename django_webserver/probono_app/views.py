from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.http import HttpResponse, JsonResponse
import requests
import xmltodict
from bson.json_util import loads, dumps
# crawling`
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
# 구글링해서 찾은것, 지울수도
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
#img_url
from urllib.parse import urljoin

# Mongo DB
from config import utils

# Session
from django.contrib.auth import login, logout

# User
from .models import CustomUser
from .forms import SignUpForm


db_handle = utils.db_handle
get_collection = utils.get_collection_handle

def index(request):
    return render(request, 'index.html')

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
    user_id = request.POST.get('username') # WARN : front's parameter name
    password = request.POST.get('password')
    user_info = users.find_one({'id' : user_id})
    if user_info:
        if (password == user_info['pw']):
            login(request, user_info)
            return redirect('index')
        else:
            data = { "message": "wrong pw" }
    else:
        data = { "message": "wrong id" }
    status_code = 201
    JsonResponse(data, status=status_code)

@require_POST
def sign_up(request):
    form = SignUpForm(request.POST)
    if form.is_valid():
        users = get_collection(db_handle, 'User')
        users.insert_one(form)
    return redirect('index')

@require_POST
def id_duplicate(request):
    users = get_collection(db_handle, 'User')
    data = loads(request.body)
    temp_id = data['check_id']
    print(temp_id)
    temp = users.find_one({'id' : temp_id})
    print('temp : ', temp)
    if not temp:
        print(temp, 'aaaaaaaaa')
        data = { 'valid' : True } # REMIND : front have to know its response.
        status_code = 201
    else:
        status_code = 201
        data = { 'valid' : False } # REMIND : front have to know its response.
    return JsonResponse(data, status=status_code)

def logout_view(request):
    logout(request)
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
    params = { 'serviceKey' : 'z3tbVitFT7XffZ43RQ9sMyE0ALiv%2BEtqOysMUKPdg9E5zTIL3lNVHqGCOS9vPqq73zYw6OhwHiskVZj4MYCJ0w%3D%3D', 'busRouteId' : '10010001' }

    response = requests.get(url, params=params)
    print(response)
    data_dict = xmltodict.parse(response.content)
    print(data_dict)
    data = data_dict.get('busRoute')
    print(data)

    return render(request, 'index.html')

def get_safety_guard_house(request):
    
    return

def crawl_notice(request, target_date):
    
    chrome_driver_path='Probono_server\django_dashboard\Scripts\chromedriver.exe'
    
    chrome_options=webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    
    site_url = "https://www.smpa.go.kr/user/nd54882.do"
    base_url = "https://www.smpa.go.kr"
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

    link_text=None
    link_url=None
    img_url=None
    if target_element:
        link = target_element.find('a')
        link_text = link.get_text()
        link_url = link['href']
    
    # 여기서 javascript함수로 되어있는 동적 정보 url로 접근해야함    
    dynamic_content=soup.find('div',class_='reply-content')
    if dynamic_content:
        print('find')
        img_url=urljoin(base_url,dynamic_content['src'])
        print(str(img_url))
    # WebDriver 종료
    driver.quit()
    
    context = {
        'link_text': link_text,
        'link_url': link_url,
        'img_url': img_url,
    }
        
    return render(request, 'crawl_result.html', context)