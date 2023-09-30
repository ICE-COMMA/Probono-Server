from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseForbidden, JsonResponse
import json
from bson.json_util import loads, dumps
from datetime import datetime

from pymongo.errors import PyMongoError
from django.core.exceptions import ObjectDoesNotExist


# Models
from .models import SpecialWeather
from .models import Bus
from .models import PopulRegion
from .models import ProbonoUser
from .models import SubwayElevator
from .models import Demo
from .models import SafetyGuardHouse

# Services
from .services import BusInfo
from .services import PopulationRealTime
from .services import PopulationAiModel

from rest_framework.response import Response
from rest_framework import generics, status
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view

from .serializers import SafetyGuardHouseSerializer
from .serializers import DemoSerializer
from .serializers import SubwayElevatorSerializer

# User
from .serializers import CreateUserSerializer, LoginUserSerializer, UserSerializer
from django.contrib.auth import login, logout
from rest_framework import permissions

class SafetyGuardHouseListView(generics.ListAPIView):
    queryset            = SafetyGuardHouse.objects.all()
    serializer_class    = SafetyGuardHouseSerializer

class DemoListView(generics.ListAPIView):
    queryset            = Demo.objects.all()
    serializer_class    = DemoSerializer

@api_view(['GET'])
def real_dense_popul_info(request):
    prt = PopulationRealTime()
    ret = prt.get_real_time_popul()
    return Response(ret)

@api_view(['GET'])
def predict_dense_popul_info(request):
    popul_ai    = PopulationAiModel()
    ret         = popul_ai.get_predict_value()
    return Response(ret)

@api_view(['GET'])
def get_bus_route(request, bus_num):
    bus_route   = BusInfo()
    data_ret    = bus_route.get_bus_route(bus_num)

    route_id        = data_ret[0]
    station_info    = data_ret[1]
    return Response({
        'route_id'  : route_id,
        'station'   : station_info
    })

@api_view(['GET'])
def get_bus_pos(request, route_id):
    bus_info    = BusInfo()
    ret         = bus_info.get_bus_pos(route_id)
    return Response(ret)

@api_view(['GET'])
def get_subway_elevator(request, subway_station):
    elevators = SubwayElevator.objects.filter(sw_nm=subway_station)
    if not elevators.exists():
        return Response(status=404)
    serializer = SubwayElevatorSerializer(elevators, many=True)
    return Response(serializer.data)

class SignUpView(generics.GenericAPIView):
    serializer_class = CreateUserSerializer

    def post(self, request, *args, **kwargs):
        data        = json.loads(request.body.decode('utf-8'))
        serializer  = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(UserSerializer(user).data)

class LoginView(generics.GenericAPIView):
    serializer_class = LoginUserSerializer

    def post(self, request, *args, **kwargs):
        data        = json.loads(request.body.decode('utf-8'))
        serializer  = self.get_serializer(data=data)

        serializer.is_valid(raise_exception=True)
        user_id = serializer.validated_data
        login(request, user_id)
        return Response(UserSerializer(user_id).data.get('name'))

class LogoutView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        print(request)
        logout(request)
        return Response(status=status.HTTP_200_OK)

class UserView(generics.RetrieveAPIView):
    permission_classes  = [permissions.IsAuthenticated]
    serializer_class    = UserSerializer

    def get_object(self):
        return self.request.user

# @api_view(['GET'])
@api_view(['POST'])
def id_check(request):
    print('ID_check : ', end='')
    data = json.loads(request.body.decode('utf-8'))
    target_id = data.get('userId')
    try:
        ProbonoUser.objects.get(ID=target_id)
        print(target_id, 'is already exist')
        data = { 'valid' : False }
    except ObjectDoesNotExist:
        print('Success')
        data = { 'valid' : True }
    return Response(data)




def index(request):
    if request.method == 'GET':
        special_weather = SpecialWeather()
        spw = special_weather.get_special_weather()
        # sess_ret = request.session.get('ID', False)
        # print('User ID :', sess_ret)
        # custom_info = False
        # if sess_ret:
            # user_collection = get_collection(db_handle, 'User')
            # temp = CustomInfo()
            # custom_info = temp.get_custom_info(sess_ret, user_collection)

        for item in spw:
            item['_id'] = str(item['_id'])
        # return JsonResponse({'user': sess_ret, 'spw': spw, 'custom': custom_info})
        return JsonResponse({'spw': spw})

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
                "success"   : True,
                "username"  : username,
                "custom"    : custom_info
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