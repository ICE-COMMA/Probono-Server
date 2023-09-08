from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
import requests
import xmltodict
from bson.json_util import loads, dumps
from datetime import datetime
import pandas as pd

# Mongo DB
from config import utils
from pymongo.errors import PyMongoError

# User
from .forms import SignUpForm

# Population_real_time
from .models import Population_real_time

db_handle = utils.db_handle
get_collection = utils.get_collection_handle

def test_AI(request):

    from .models import Population_AI_model
    popul_ai = Population_AI_model()
    popul_ai.update_population_AI()
    
    return JsonResponse({ 'popul_ai' : popul_ai})

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
            elif update_result.modified_count == 0:
                return JsonResponse({ 'valid' : False, 'error' : 'Not modified' })
            return JsonResponse({ 'valid' : True })
    except PyMongoError:
        return JsonResponse({'valid' : False, 'error': 'Database error'})

def transfer_info(request):
    return render(request, 'transfer_info.html')

def weather_info(request):
    return render(request, 'weather_info.html')

def dense_popul_info(request):
    
    if request.method == 'GET':
        prt = Population_real_time()
        collection = get_collection(db_handle, 'popul_real_time_reg')
        region_info = list(collection.find({}))
        ret = prt.get_real_time_popul(region_info)
        return JsonResponse({ 'ret' : ret })
    # return render(request, 'dense_popul_info.html')
    # return render(request, 'index.html')

def get_hot_place(request):
    # if 
    return render(request, 'index.html')

def safety_info(request):
    return render(request, 'safety_info.html')

def safety_info_data(request):
    collection = get_collection(db_handle, 'safety_guard_house')
    ret = collection.find()
    ret_list = [{'name': item['name'], 'x': item['y'], 'y': item['x']} for item in ret]
    return JsonResponse({ 'ret' : ret_list })
    

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
    temp = users.find_one({ 'ID' : temp_id })
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
    collection = get_collection(db_handle, 'demo')
    ret = list(collection.find({}))
    print(ret)
    return render(request, 'demo.html', { 'demo' : ret })