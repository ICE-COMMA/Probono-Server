from rest_framework import serializers


from .models import SpecialWeather
from .models import Bus
from .models import PopulRegion
from .models import User
from .models import SubwayElevator
from .models import Demo
from .models import SafetyGuardHouse

class SpecialWeatherSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpecialWeather
        fields = '__all__'

class DemoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Demo
        fields = ['location', 'date', 'time', 'amount']

class SafetyGuardHouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = SafetyGuardHouse
        fields = ['name', 'x', 'y']

class SubwayElevatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubwayElevator
        fields = ['sw_nm', 'x', 'y']