from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.http import HttpResponse, JsonResponse
import requests
import xmltodict
from bson.json_util import loads, dumps
from datetime import datetime

from .models import SpecialWeather
# crawling`
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
import fitz # PyMuPDF 라이브러리 모듈
import os
from django.http import HttpResponse
#img 처리
import pytesseract
from PIL import Image
import cv2 # img 내 테이블 처리(전처리)
import numpy as np

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


def my_page(request, id):
    if request.method == 'GET':
        collection = get_collection(db_handle, 'User')
        ret = collection.find_one({'ID' : id})
        if not ret:
            return HttpResponse("Can not find user.")
        return render(request, 'my_page.html', { 'info' : ret })
    elif request.method == 'POST':
        collection = get_collection(db_handle, 'User')
        data = loads(request.body)
        collection.update_one({ 'ID' : id }, { '$set' : { data } })
        ret = { 'valid' : True }
        return JsonResponse(ret)

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

def get_bus_route(request):

    # collection_bus = get_collection(db_handle, 'bus')
    # num = request.POST.get('bus_num')
    # route = collection_bus.find_one(num)
    route = 100100001
    url = 'http://ws.bus.go.kr/api/rest/busRouteInfo/getStaionByRoute'
    params = { 'ServiceKey' : '4cwiloFmPQxO3hXwmJy3jruoPPh6m8PQZqxBkWecSAgIIeRjq6UIdo0r7ZnmT4Rm4kVErRaD9jd1XU5CS7Chwg==', 'busRouteId' : str(route), 'resultType' : 'json' }

    response = requests.get(url, params=params)
    print(response)
    data = response.json()
    print(data)
    item_list = data['msgBody']['itemList']
    print(item_list[0])
    print(item_list[1])
    # print(response.content)
    # data_dict = xmltodict.parse(response.content)
    # print(data_dict)
    # data = data_dict.get('busRoute')
    # print(data)

    return render(request, 'index.html')

def get_safety_guard_house(request):
    
    return

def get_demo_today(request):
    
    download_path='C:\\Users\\admin\\Downloads'
    driver_path = os.path.realpath('chromedriver.exe')
    s=Service('C:\\Probono_server\\server\\django_dashboard\\Scripts\\chromedriver.exe')
    print(driver_path+'\n')
    
    chrome_options=webdriver.ChromeOptions()
    # chrome 창 안보이게
    # chrome_options.add_argument("--headless")
    # chrome 다운로드 경로 설정
    chrome_options.add_experimental_option("prefs",{
        #"download.default_directory":download_path,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True,
        "profile.default_content_settings.popups": 0
        })
    
    #driver = webdriver.Chrome(service=s,options=chrome_options)
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
    link_text="오늘의 집회"
    date=year+current_date.strftime("%m%d") # 원하는 날짜로 보려면 target_date로 받아야함
    blank=" "
    xpath_expression = f"//a[contains(text(),'{link_text}{blank}{date}{blank}{day}')]"
    element = driver.find_element(By.XPATH, xpath_expression)
    driver.execute_script("arguments[0].scrollIntoView();", element) #해당 요소로 스크롤 이동
    
    # 새 페이지로 이동
    element.click()
    current_url=driver.current_url
    
    # 대기시간
    wait = WebDriverWait(driver, 10)
    
    target_filename=date+"("+day+")"+blank+"인터넷집회.pdf"
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
        wait.until(lambda driver: target_filename in os.listdir('C:\\Users\\admin\\Downloads'))

    
    # 이미지 요소의 XPath로 이미지를 찾고, src 속성을 가져옴
    image_element = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='bcontent']//img")))
    image_url = image_element.get_attribute("src")    
    
    # WebDriver 종료
    driver.quit()
    
    # PDF에서 텍스트 추출
    pdf_path = 'C:\\Users\\admin\\Downloads\\230822(화) 인터넷집회.pdf'  # 실제 PDF 파일의 경로로 바꾸세요

    try:
        # PDF 파일 열기
        pdf_document = fitz.open(pdf_path)

        extracted_text = ''

        # 잘 열리는지 페이지 수로 확인
        num_pg=pdf_document.page_count
                
        # 모든 페이지에 대해 텍스트 추출
        for page_num in range(num_pg):
            page = pdf_document.load_page(page_num)
            extracted_text = page.get_text()

        # 추출된 텍스트를 컨텍스트에 담아서 템플릿으로 전달
        context = {
            'extracted_text': extracted_text,
            'page_num':num_pg,
            'driver_path':driver_path,
            'pdf_path' : download_path,
            'filename' : target_filename,
            'link_url': current_url,
            'img_url': image_url,
        }
        return render(request, 'crawl_result.html', context)
    
    except Exception as e:
        return HttpResponse(f"오류 발생: {e}")
    finally:
        pdf_document.close()  # 파일을 열었으면 꼭 닫아줍니다.
    
def get_text_from_image(request):
    
    current_date=datetime.now()
    year=current_date.strftime("%y")
    today=current_date.weekday()
    days=["월","화","수","목","금","토","일"]
    day=days[today]
    date=year+current_date.strftime("%m%d") # 원하는 날짜로 보려면 target_date로 받아야함
    blank=" "
    img_name=date+"("+day+")"+blank+"인터넷집회001.jpg"
    new_name=date+"demo.jpg"
    
    img_path='C:/Users/admin/Downloads/'+ img_name
    new_img_path=os.path.join(os.path.dirname(img_path),new_name)
    # #이 작업은 한번만 진행
    # os.rename(img_path,new_img_path)
    
    tesseract_path = 'C:\\Probono_server\\server\\django_dashboard\\Lib\\site-packages\\pytesseract\\pytesseract.py'  # 가상환경 경로에 맞게 수정
    
    image=cv2.imread(new_img_path)
    print(image.shape)
    
    # 특정 영역의 마스크 생성
    mask = np.zeros(image.shape[:2], dtype=np.uint8)
    roi = (0, 0, 900, 200)  # 특정 영역의 좌표
    mask[0:200, 0:992] = 255
        
    # img 전처리(그레이스케일: 흑백으로 전환)
    gray=cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # # 흑백 이미지 확인
    # cv2.imshow('Grayscale Image',gray)
    
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    
    # # 경계선 감지 (예: Canny Edge Detection)
    # edges = cv2.Canny(gray, threshold1=10, threshold2=100)
    
    # # 경계선으로 컨투어 찾기
    # contours, _ = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # 임계값 처리
    _, thresholded = cv2.threshold(gray, 216, 255, cv2.THRESH_BINARY)
    # 반전
    thresholded=~thresholded

    
    line_min_width=50
    kernel_h=np.ones((1,line_min_width),np.uint8)
    kernel_v=np.ones((line_min_width,1),np.uint8)
    
    img_bin_h=cv2.morphologyEx(thresholded,cv2.MORPH_OPEN, kernel_h)
    img_bin_v=cv2.morphologyEx(thresholded,cv2.MORPH_OPEN, kernel_v)
    
    img_bin_final=img_bin_h|img_bin_v
    
    cv2.imshow('Grayscale Image',img_bin_final)
    
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    print(img_bin_final.shape)
    
    # 윤곽선 검출
    contours, _ = cv2.findContours(img_bin_final, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE,mask=mask)
    
    print(len(contours))
    # 테이블 영역 추출
    table_contours = []
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 210000 and area < 840000:
            table_contours.append(contour)
            
    result=image.copy()
    cv2.drawContours(result,contours,-1,(0,255,0),2)
    cv2.imwrite('result_image.jpg',result)

    # 테이블 영역 잘린 이미지 생성
    table_images = []
    for contour in table_contours:
        x, y, w, h = cv2.boundingRect(contour)
        table_images.append(image[y:y+h, x:x+w])
    
    # 실험
    oem=1
    extracted_text=""
    try:
        for table_image in table_images:
            # img 전처리
            gray_table=cv2.cvtColor(table_image,cv2.COLOR_BGR2GRAY)
            cell_text = pytesseract.image_to_string(Image.fromarray(gray_table), lang='kor',config=f'-c tessedit_ocr_engine_mode={oem}')
            
            extracted_text+=cell_text+'\n'
        context = {
            'extracted_text': extracted_text
        }
        return render(request, 'get_image.html',context)
    
    except Exception as e:
        return HttpResponse(str(e))
    
    # # 원래거
    # oem=1
    # try:
    #     extracted_text = pytesseract.image_to_string(Image.open(img_path), lang='kor',config=f'-c tessedit_ocr_engine_mode={oem}')
    #     context = {
    #         'extracted_text': extracted_text
    #     }
    #     return render(request, 'get_image.html',context)
    
    # except Exception as e:
    #     return HttpResponse(str(e))