from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from geo.models import City
from geoAPI.serializers import (
    CitySerializer,
    CityQuerySerializer,
    CityCountSerializer,
)


class CityAPITestCase(APITestCase):
    def setUp(self):
        # Создание тестовых данных
        self.city1 = City.objects.create(
            name='Moscow',
            latitude=55.7558,
            longitude=37.6176,
            request_count=10,
        )
        self.city2 = City.objects.create(
            name='Saint Petersburg',
            latitude=59.9343,
            longitude=30.3351,
            request_count=5,
        )
        self.city3 = City.objects.create(
            name='Novosibirsk',
            latitude=55.0084,
            longitude=82.9357,
            request_count=0,
        )

    def test_city_list(self):
        url = reverse('city-list')
        response = self.client.get(url)
        cities = City.objects.all()
        serializer = CitySerializer(cities, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_city_search(self):
        url = reverse('city-search')
        response = self.client.get(url, {'city': 'Moscow'})
        cities = City.objects.filter(name__icontains='Moscow')
        serializer = CityQuerySerializer(cities, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_city_search_no_query(self):
        url = reverse('city-search')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data,
            {'error': 'Query parameter is required'},
        )

    def test_city_count(self):
        url = reverse('city-count')
        response = self.client.get(url)
        cities = City.objects.filter(request_count__gt=0)
        serializer = CityCountSerializer(cities, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_city_count_empty(self):
        City.objects.filter(request_count__gt=0).delete()
        url = reverse('city-count')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    def test_city_detail(self):
        url = reverse('city-detail', args=[self.city1.id])
        response = self.client.get(url)
        serializer = CitySerializer(self.city1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_city_update(self):
        url = reverse('city-detail', args=[self.city1.id])
        data = {'name': 'Updated Moscow'}
        response = self.client.patch(url, data, format='json')
        self.city1.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.city1.name, 'Updated Moscow')

    def test_city_create(self):
        url = reverse('city-list')
        data = {
            'name': 'Kazan',
            'latitude': 55.8304,
            'longitude': 49.0661,
            'request_count': 1,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(City.objects.count(), 4)
        self.assertEqual(City.objects.last().name, 'Kazan')

    def test_city_delete(self):
        url = reverse('city-detail', args=[self.city3.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(City.objects.count(), 2)
