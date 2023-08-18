from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.http import HttpResponse, JsonResponse
import requests
import xmltodict
from bson.json_util import loads, dumps

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
def id_check(request):
    users = get_collection(db_handle, 'User')
    data = loads(request.body)
    temp_id = data['check_id']
    temp = users.find_one({'id' : temp_id})
    if not temp:
        print(temp, 'result : True!!')
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
    params = { 'serviceKey' : '4cwiloFmPQxO3hXwmJy3jruoPPh6m8PQZqxBkWecSAgIIeRjq6UIdo0r7ZnmT4Rm4kVErRaD9jd1XU5CS7Chwg==', 'busRouteId' : str(route) }

    response = requests.get(url, params=params)
    print(response)
    data_dict = xmltodict.parse(response.content)
    print(data_dict)
    data = data_dict.get('busRoute')
    print(data)

    return render(request, 'index.html')

def get_safety_guard_house(request):
    
    
    
    
    
    return render(request, 'index.html')
