import urllib
from unittest.mock import patch

import requests
from django.test import Client
from django.test import TestCase
from django.urls import reverse

from geo.models import City
from geo.views import (
    get_lat_lon_by_ip,
    get_city_by_lat_lon,
    get_weather_by_lat_lot,
    APIRequestException,
)


class GetLatLonByIpTest(TestCase):
    @patch('geo.views.requests.post')
    def test_get_lat_lon_by_ip_success(self, mock_post):
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            'position': {'latitude': 55.7558, 'longitude': 37.6176},
        }
        lat, lon = get_lat_lon_by_ip('8.8.8.8')
        self.assertEqual(lat, 55.7558)
        self.assertEqual(lon, 37.6176)

    @patch('geo.views.requests.post')
    def test_get_lat_lon_by_ip_failure(self, mock_post):
        mock_post.side_effect = requests.exceptions.RequestException
        with self.assertRaises(APIRequestException):
            get_lat_lon_by_ip('8.8.8.8')


class GetCityByLatLonTest(TestCase):
    @patch('geo.views.requests.get')
    def test_get_city_by_lat_lon_success(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            'response': {
                'GeoObjectCollection': {
                    'featureMember': [
                        {
                            'GeoObject': {
                                'metaDataProperty': {
                                    'GeocoderMetaData': {
                                        'Address': {
                                            'Components': [
                                                {
                                                    'kind': 'locality',
                                                    'name': 'Moscow',
                                                },
                                            ],
                                        },
                                    },
                                },
                            },
                        },
                    ],
                },
            },
        }
        city = get_city_by_lat_lon(55.7558, 37.6176)
        self.assertEqual(city, 'Moscow')

    @patch('geo.views.requests.get')
    def test_get_city_by_lat_lon_failure(self, mock_get):
        mock_get.side_effect = requests.exceptions.RequestException
        with self.assertRaises(APIRequestException):
            get_city_by_lat_lon(55.7558, 37.6176)


class GetWeatherByLatLonTest(TestCase):
    @patch('geo.views.requests.get')
    def test_get_weather_by_lat_lon_success(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            'forecasts': [
                {'date': '2024-07-20', 'parts': {'day': {'temp_avg': 20}}},
                {'date': '2024-07-21', 'parts': {'day': {'temp_avg': 22}}},
            ],
        }
        forecast = get_weather_by_lat_lot(55.7558, 37.6176)
        self.assertEqual(len(forecast), 2)

    @patch('geo.views.requests.get')
    def test_get_weather_by_lat_lon_failure(self, mock_get):
        mock_get.side_effect = requests.exceptions.RequestException
        with self.assertRaises(APIRequestException):
            get_weather_by_lat_lot(55.7558, 37.6176)


class GeoViewTest(TestCase):
    @patch('geo.views.get_lat_lon_by_ip')
    @patch('geo.views.get_city_by_lat_lon')
    @patch('geo.views.get_weather_by_lat_lot')
    def test_geo_view_success(self, mock_weather, mock_city, mock_ip):
        mock_ip.return_value = (55.7558, 37.6176)
        mock_city.return_value = 'Moscow'
        mock_weather.return_value = [
            {'date': '2024-07-20', 'parts': {'day': {'temp_avg': 20}}},
        ]

        City.objects.create(name='Moscow', latitude=55.7558, longitude=37.6176)

        client = Client()
        response = client.get(reverse('geo:geo-auto'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Moscow')
        self.assertContains(response, '20')


class GeoDetailViewTest(TestCase):
    @patch('geo.views.get_weather_by_lat_lot')
    def test_geo_detail_view_success(self, mock_weather):
        mock_weather.return_value = [
            {'date': '2024-07-20', 'parts': {'day': {'temp_avg': 20}}},
        ]

        city = City.objects.create(
            name='Moscow',
            latitude=55.7558,
            longitude=37.6176,
        )

        client = Client()
        response = client.get(reverse('geo:geo-detail', args=[city.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Moscow')
        self.assertContains(response, '20')

        city.refresh_from_db()
        self.assertEqual(city.request_count, 1)


class SelectedCitiesCookieTest(TestCase):
    def test_update_selected_cities_cookie(self):
        city = City.objects.create(
            name='Moscow',
            latitude=55.7558,
            longitude=37.6176,
        )
        client = Client()
        response = client.get(reverse('geo:geo-detail', args=[city.id]))
        self.assertEqual(
            response.cookies['selected_cities'].value,
            urllib.parse.quote('Moscow'),
        )
