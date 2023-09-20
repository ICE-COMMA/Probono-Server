from rest_framework import serializers
from .models import Safety_Guard_House, Police_Station


class Safety_Guard_House_Serializers(serializers.ModelSerializer):
    class Meta:
        model = Safety_Guard_House
        fields = ['name', 'x', 'y']


class Police_Station_Serializers(serializers.ModelSerializer):
    class Meta:
        model = Police_Station
        fields = ['stat_name', 'x', 'y']
