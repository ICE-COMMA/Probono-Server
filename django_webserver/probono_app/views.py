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
    queryset = SafetyGuardHouse.objects.all()
    serializer_class = SafetyGuardHouseSerializer


class DemoListView(generics.ListAPIView):
    queryset = Demo.objects.all()
    serializer_class = DemoSerializer


@api_view(['GET'])
def real_dense_popul_info(request):
    prt = PopulationRealTime()
    ret = prt.get_real_time_popul()
    return Response(ret)


@api_view(['GET'])
def predict_dense_popul_info(request):
    popul_ai = PopulationAiModel()
    ret = popul_ai.get_predict_value()
    return Response(ret)


@api_view(['GET'])
def get_bus_route(request, bus_num):
    bus_route = BusInfo()
    data_ret = bus_route.get_bus_route(bus_num)

    route_id = data_ret[0]
    station_info = data_ret[1]
    return Response({
        'route_id': route_id,
        'station': station_info
    })


@api_view(['GET'])
def get_bus_pos(request, route_id):
    bus_info = BusInfo()
    ret = bus_info.get_bus_pos(route_id)
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
        data = json.loads(request.body.decode('utf-8'))
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(UserSerializer(user).data)


class LoginView(generics.GenericAPIView):
    serializer_class = LoginUserSerializer

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body.decode('utf-8'))
        serializer = self.get_serializer(data=data)

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
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

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
        data = {'valid': False}
    except ObjectDoesNotExist:
        print('Success')
        data = {'valid': True}
    return Response(data)