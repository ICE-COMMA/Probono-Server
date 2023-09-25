from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseForbidden, JsonResponse
import requests
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

# Population_real_time, predict
from .models import Population_real_time
from .models import Population_AI_model

from .models import Custom_info

from .models import Subway_info

from .models import DemoInfo



db_handle = utils.db_handle
get_collection = utils.get_collection_handle


def test_AI(request):

    from .models import Population_AI_model
    popul_ai = Population_AI_model()
    ret = popul_ai.get_predict_value()

    return JsonResponse({'popul_ai': ret})


def index(request):
    if request.method == 'GET':
        weather_collection = get_collection(db_handle, 'special_weather')
        special_weather_info = list(weather_collection.find({}))
        sess_ret = request.session.get('ID', False)
        print('User ID :', sess_ret)
        custom_info = False
        if sess_ret:
            user_collection = get_collection(db_handle, 'User')
            temp = Custom_info()
            custom_info = temp.get_custom_info(sess_ret, user_collection)

        for item in special_weather_info:
            item['_id'] = str(item['_id'])
        return JsonResponse({'user': sess_ret, 'spw': special_weather_info, 'custom': custom_info})

    # elif request.method == 'POST':
    #     collection = get_collection(db_handle, 'report')
    #     data = loads(request.body)
    #     print('TEST : ', data, '\n', 'TYPE : ', type(data))
    #     # collection.insert_one()


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
            return JsonResponse({'info': ret})
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


@require_GET
def real_dense_popul_info(request):
    prt = Population_real_time()
    collection = get_collection(db_handle, 'popul_real_time_reg')
    region_info = list(collection.find({}))
    ret = prt.get_real_time_popul(region_info)
    return JsonResponse({'real_time': ret})


@require_GET
def predict_dense_popul_info(request):
    popul_ai = Population_AI_model()
    ret = popul_ai.get_predict_value()
    return JsonResponse({'predict': ret})


@require_GET
def safety_info_data(request):
    collection = get_collection(db_handle, 'safety_guard_house')
    ret = collection.find()
    ret_list = [{'name': item['name'], 'x': item['y'], 'y': item['x']}
                for item in ret]
    return JsonResponse({'ret': ret_list})


@csrf_exempt
@require_POST
def login_view(request):
    data = json.loads(request.body.decode('utf-8'))
    users = get_collection(db_handle, 'User')
    user_id = data.get('id')  # WARN : front's parameter name
    password = data.get('password')
    user_info = users.find_one({'ID': user_id})
    # print(user_info)
    print('Login : ', end='')
    if user_info:
        username = user_info['name']
        if password == user_info['PW']:
            request.session['ID'] = user_id  # session에 로그인한 user의 id저장
            custom_info = user_info.get('custom', {})
            # print(custom_info)
            # print(request.session.items())
            data = {
                "success": True,
                "username": username,
                "custom": custom_info
            }
            print(user_id)
            status_code = 200
        else:
            data = {"success": False}
            print('Invalid password')
            status_code = 401
    else:
        data = {"success": False}
        print("Invalid ID")
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


@csrf_exempt
@require_POST
def id_check(request):
    users = get_collection(db_handle, 'User')
    data = json.loads(request.body)
    temp_id = data['userId']
    print('ID_check : ', end='')
    temp = users.find_one({'ID': temp_id})
    if not temp:
        print('Success')
        data = {'valid': True}  # REMIND : front have to know its response.
        status_code = 200
    else:
        print(temp_id, 'is already exist')
        status_code = 200
        data = {'valid': False}  # REMIND : front have to know its response.
    return JsonResponse(data, status=status_code)


def logout_view(request):
    request.session.flush()
    return


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


@require_GET
def get_subway_elvtr(request, subway_station):
    subway_info = Subway_info()
    elevator_data = subway_info.get_subway_elvtr(subway_station)
    return JsonResponse(elevator_data)

@require_GET
def get_bus_route(request, bus_num):
    bus_route = Bus_info()
    data_ret = bus_route.get_bus_route(bus_num)

    route_id = data_ret[0]
    station_info = data_ret[1]
    return JsonResponse({'route_id' : route_id, 'station' : station_info})


@require_GET
def get_bus_pos(request, route_id):
    bus_info = Bus_info()
    ret = bus_info.get_bus_pos(route_id)
    return JsonResponse({'bus_pos': ret})


@require_GET
def get_demo_today(request):
    # collection = get_collection(db_handle, 'demo')
    # data_demo = list(collection.find({}))
    # ret = []
    # for item in data_demo:
    #     item_data = {
    #         "location": str(item["location"]),
    #         "date": str(item["date"]),
    #         "time": str(item["time"]),
    #         "amount": str(item["amount"])
    #     }
    #     ret.append(item_data)
    demo_info = DemoInfo()
    ret = demo_info.get_demo_info()
    return JsonResponse({'demo': ret})