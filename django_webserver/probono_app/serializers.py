from rest_framework import serializers


from .models import SpecialWeather
from .models import Bus
from .models import PopulRegion

from .models import ProbonoUser, CustomPreferences
from django.contrib.auth import authenticate

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
        
class CustomPreferencesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomPreferences
        # fields = '__all__'
        fields = [
            'custom_demo', 'custom_elevator', 'custom_population', 
            'custom_predict', 'custom_safety', 'custom_safety_loc',
            'custom_low_bus', 'custom_festival'
        ]

class CreateUserSerializer(serializers.ModelSerializer):
    userId = serializers.CharField(source='ID')
    userName = serializers.CharField(source='name')
    birth = serializers.DateField(source='date')

    class Meta:
        model = ProbonoUser
        fields = ['userId', 'userName', 'password', 'gender', 'birth', 'impaired']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):

        custom_preferences = CustomPreferences.objects.create()
        validated_data['custom'] = custom_preferences
        user = ProbonoUser.objects.create_user(
            ID=validated_data['ID'],
            password=validated_data['password'],
            name=validated_data['name'],
            gender=validated_data['gender'],
            date=validated_data['date'],
            impaired=validated_data['impaired'],
            custom = validated_data['custom']
        )
        return user

class UserSerializer(serializers.ModelSerializer):
    custom = CustomPreferencesSerializer()

    class Meta:
        model = ProbonoUser
        fields = ['ID', 'name', 'gender', 'date', 'impaired', 'custom']

class LoginUserSerializer(serializers.Serializer):
    ID = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError('Login : Fail')