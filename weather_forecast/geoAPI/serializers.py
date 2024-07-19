from rest_framework import serializers

from geo.models import City


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'


class CityQuerySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id', 'name']


class CityCountSerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['name', 'request_count']
