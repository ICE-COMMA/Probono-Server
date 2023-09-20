from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
import requests
import xmltodict
import json
from bson.json_util import loads, dumps
from datetime import datetime

# Mongo DB
from config import utils
from pymongo.errors import PyMongoError

# User
from .forms import SignUpForm

# Transfer info
from .models import Bus_info

# Population_real_time
from .models import Population_real_time

db_handle = utils.db_handle
get_collection = utils.get_collection_handle


def test_AI(request):

    from .models import Population_AI_model
    popul_ai = Population_AI_model()
    ret = popul_ai.return_predict_value()

    return JsonResponse({'popul_ai': ret}, safe=False)


def test_bus(request):

    temp = Bus_info()
    ret = temp.get_bus_pos('100100410')

    return JsonResponse({'bus_pos': ret})


def index(request):
    if request.method == 'GET':
        collection = get_collection(db_handle, 'special_weather')
        ret = list(collection.find({}))
        sess_ret = request.session.get('ID', False)
        # MongoDB의 _id는 JSON serializable하지 않기 때문에 문자열로 변환
        for item in ret:
            item['_id'] = str(item['_id'])
        return JsonResponse({'user': sess_ret, 'spw': ret})

    elif request.method == 'POST':
        collection = get_collection(db_handle, 'report')
        data = loads(request.body)
        print('TEST : ', data, '\n', 'TYPE : ', type(data))
        # collection.insert_one()


def my_page(request, id):
    try:
        current_user_id = request.session.get('ID', None)
        if not current_user_id:
            return HttpResponseForbidden("ACCESS DENIED")
        if request.method == 'GET':
            collection = get_collection(db_handle, 'User')
            ret = collection.find_one({'ID': id})
            if not ret or str(ret['ID']) != str(current_user_id):
                return HttpResponseForbidden("ACCESS DENIED")
            formatted_date = ret['date'].strftime('%Y.%m.%d')
            ret['date'] = formatted_date
            print(ret)
            return render(request, 'my_page.html', {'info': ret})
        elif request.method == 'POST':
            if str(id) != str(current_user_id):
                return HttpResponseForbidden("ACCESS DENIED")
            collection = get_collection(db_handle, 'User')
            data = loads(request.body)
            print(data)

            new_data = {
                'PW': data['next_pw'],
                'impaired': data['user_handicap']
            }
            print(new_data)
            update_result = collection.update_one(
                {'ID': id}, {'$set': new_data})
            if update_result.matched_count == 0:
                return JsonResponse({'valid': False, 'error': 'Not found'})
            elif update_result.modified_count == 0:
                return JsonResponse({'valid': False, 'error': 'Not modified'})
            return JsonResponse({'valid': True})
    except PyMongoError:
        return JsonResponse({'valid': False, 'error': 'Database error'})


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
        return JsonResponse({'ret': ret})


def get_hot_place(request):
    # if
    return render(request, 'index.html')


def safety_info(request):
    return render(request, 'safety_info.html')


def safety_info_data(request):
    collection = get_collection(db_handle, 'safety_guard_house')
    ret = collection.find()
    ret_list = [{'name': item['name'], 'x': item['y'], 'y': item['x']}
                for item in ret]
    return JsonResponse({'ret': ret_list})


@csrf_exempt
@require_POST
def login_view(request):
    print(request.body)
    data = json.loads(request.body.decode('utf-8'))
    users = get_collection(db_handle, 'User')
    user_id = data.get('id')  # WARN : front's parameter name
    password = data.get('password')
    user_info = users.find_one({'ID': user_id})
    username = user_info['name']
    if user_info:
        if password == user_info['PW']:
            request.session['ID'] = user_id  # session에 로그인한 user의 id저장
            print(request.session.items())
            data = {
                "success": True,
                "username": username
            }
            status_code = 200
        else:
            data = {"success": False}
            print("wrong pw")
            status_code = 401
    else:
        data = {"success": False}
        print("no id")
        status_code = 401

    return JsonResponse(data, status=status_code)


@require_POST
def sign_up(request):
    data = json.loads(request.body.decode('utf-8'))

    print(data)
    # date_obj = data.get('date')
    # datetime_obj = datetime(date_obj.year, date_obj.month, date_obj.day)

    default_custom_settings = {
        "custom-demo": False,
        "custom-elevator": False,
        "custom-population": False,
        "custom-predict": False,
        "custom-safety": False,
        "custom-safey-loc": False,
        "custom-low-bus": False,
        "custom-festival": False
    }

    user_data = {
        "ID": data.get('userId'),
        "name": data.get('userName'),
        "PW": data.get('password'),
        "gender": data.get('gender'),
        "date": data.get('birth'),
        "impaired": data.get('impaired'),
        "custom": default_custom_settings  # custom 필드는 빈 문자열로 초기화
    }
    try:
        users = get_collection(db_handle, 'User')
        users.insert_one(user_data)

        return JsonResponse({'success': True, 'message': '회원가입에 성공하였습니다.'})

    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})
    # print(request.POST)
    # form = SignUpForm(request.POST)
    # if form.is_valid():
    #     print('GOOD')
    #     user_data = form.cleaned_data
    #     date_obj = form.cleaned_data['date']
    #     datetime_obj = datetime(date_obj.year, date_obj.month, date_obj.day)
    #     form.cleaned_data['date'] = datetime_obj
    #     user_data['custom'] = ''
    #     print(user_data)
    #     users = get_collection(db_handle, 'User')
    #     users.insert_one(form.cleaned_data)
    #     return redirect('index')
    # print(form.errors)
    # ret = {'message': 'error'}
    # return JsonResponse(ret)


@require_POST
def id_check(request):
    users = get_collection(db_handle, 'User')
    data = json.loads(request.body)
    temp_id = data['userId']
    print(request.body)
    temp = users.find_one({'ID': temp_id})
    if not temp:
        data = {'valid': True}  # REMIND : front have to know its response.
        status_code = 200
    else:
        print("already ID")
        status_code = 200
        data = {'valid': False}  # REMIND : front have to know its response.
    return JsonResponse(data, status=status_code)


def logout_view(request):
    request.session.flush()
    return redirect('index')


@csrf_exempt
@require_POST
def update_custom(request):

    try:
        data = loads(request.body)  # select 정보 가져오기
        user_id = request.session.get('ID')  # 세션을 통해 uesr_id가져오기

        custom_data = data.get('select', {})
        users = get_collection(db_handle, 'User')
        users.update_one({'ID': user_id}, {"$set": {'custom': custom_data}})

        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False})


@require_POST
def get_subway_elvtr(request):
    collection_elvtr = get_collection(db_handle, 'subway_elevator')
    search = request.POST.get('name')
    result = collection_elvtr.find({'sw_nm': search})
    result = list(result)
    if not result:
        return JsonResponse({'message': 'No results'})
    return JsonResponse({'result': result})


def get_bus_no_to_route(request):

    return


def get_bus_route(request, bus_num):

    collection_bus = get_collection(db_handle, 'bus')
    bus_info = collection_bus.find_one({'bus_no': bus_num})
    url = 'http://ws.bus.go.kr/api/rest/busRouteInfo/getStaionByRoute'
    key = '4cwiloFmPQxO3hXwmJy3jruoPPh6m8PQZqxBkWecSAgIIeRjq6UIdo0r7ZnmT4Rm4kVErRaD9jd1XU5CS7Chwg=='
    params = {'ServiceKey': key,
              'busRouteId': bus_info['route'], 'resultType': 'json'}

    response = requests.get(url, params=params)
    print(response)
    data = response.json()
    item_list = data['msgBody']['itemList']

    ret = []
    for target in item_list:
        data = {
            'station_id': target['station'],
            'name': target['stationNm'],
            'seq': target['seq'],
            'x': target['gpsX'],
            'y': target['gpsY']
        }
        print(data)
        ret.append(data)
    return JsonResponse({'station': ret})


def get_safety_guard_house(request):

    return


def get_demo_today(request):
    collection = get_collection(db_handle, 'demo')
    ret = list(collection.find({}))
    # print(ret)
    # return render(request, 'demo.html', {'demo': ret})

    # react에 맞게 api 엔드포인트 생성
    ret = []
    for item in ret:
        item_data = {
            "location": str(item["location"]),
            "date": str(item["date"]),
            "time": str(item["time"]),
            "amount": str(item["amount"])
        }
        ret.append(item_data)

    return JsonResponse({'demo': ret})
