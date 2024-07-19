import json
import os
import urllib

import django.views.generic
import requests
from django.shortcuts import get_object_or_404
from ipware.ip import get_client_ip

import geo.models
from geo.exceptions import APIRequestException


def get_lat_lon_by_ip(ip: str) -> [float, float]:
    url = 'http://api.lbs.yandex.net/geolocation'
    data = json.dumps(
        {
            'common': {
                'version': '1.0',
                'api_key': os.getenv('API_KEY_LOCATOR'),
            },
            'ip': {'address_v4': ip},
        },
    )
    try:
        response = requests.post(url, files={'json': (None, data)})
        response.raise_for_status()
        response_data = response.json()['position']
        return response_data['latitude'], response_data['longitude']
    except Exception as e:
        raise APIRequestException(e)


def get_city_by_lat_lon(lat: float, lon: float):
    api_key = os.getenv('API_KEY_GEOCODER')
    url = (
        f'https://geocode-maps.yandex.ru/1.x/?apikey={api_key}&geocode='
        f'{lon},{lat}&format=json&results=1'
    )
    try:
        response = requests.get(url)
        response.raise_for_status()
        response_data = response.json()
        components = response_data['response']['GeoObjectCollection'][
            'featureMember'
        ][0]['GeoObject']['metaDataProperty']['GeocoderMetaData']['Address'][
            'Components'
        ]
        city = list(filter(lambda x: x['kind'] == 'locality', components))[0][
            'name'
        ]
        return city
    except Exception as e:
        raise APIRequestException(e)


def get_weather_by_lat_lot(lat: float, lon: float):
    access_key = os.getenv('API_KEY_WEATHER')

    headers = {'X-Yandex-Weather-Key': access_key}

    try:
        response = requests.get(
            f'https://api.weather.yandex.ru/v2/forecast?lat={lat}&lon={lon}',
            headers=headers,
        )
        response.raise_for_status()
        weather_data = response.json()
        forecast_data = weather_data['forecasts']
        return forecast_data[:7]
    except Exception as e:
        raise APIRequestException(e)


def update_get_selected_cities(request, city):
    selected_cities = request.COOKIES.get('selected_cities', '')
    selected_cities = urllib.parse.unquote(selected_cities)
    if city.name not in selected_cities:
        selected_cities = (
            f'{selected_cities},{city.name}' if selected_cities else city.name
        )
    return selected_cities


class GeoView(django.views.generic.TemplateView):
    template_name = 'geo/weather.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        ip, _ = get_client_ip(self.request)
        try:
            lat, lon = get_lat_lon_by_ip(ip)
            city = get_city_by_lat_lon(lat, lon)
            seven_day_forecast = get_weather_by_lat_lot(lat, lon)
        except APIRequestException:
            city = geo.models.City.objects.get(name='Москва')
            seven_day_forecast = get_weather_by_lat_lot(
                city.latitude, city.longitude,
            )

        context['city'] = city
        context['ten_day_forecast'] = seven_day_forecast

        selected_cities = self.request.COOKIES.get('selected_cities', '')
        selected_cities = urllib.parse.unquote(selected_cities)
        selected_cities_list = selected_cities.split(',')
        cities_user = geo.models.City.objects.filter(
            name__in=selected_cities_list,
        )
        context['cities_user'] = cities_user

        return context


class GeoDetailView(django.views.generic.DetailView):
    model = geo.models.City
    template_name = 'geo/weather.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        pk = self.kwargs.get('pk')
        city = get_object_or_404(self.model, pk=pk)
        city.request_count += 1
        city.save()

        seven_day_forecast = get_weather_by_lat_lot(
            city.latitude, city.longitude,
        )
        selected_cities = update_get_selected_cities(self.request, city)
        selected_cities_list = selected_cities.split(',')
        cities_user = geo.models.City.objects.filter(
            name__in=selected_cities_list,
        )
        context['cities_user'] = cities_user
        context['city'] = city.name
        context['ten_day_forecast'] = seven_day_forecast

        context['selected_cities'] = selected_cities
        return context

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        response = self.render_to_response(context)
        selected_cities_encoded = urllib.parse.quote(
            context['selected_cities'],
        )
        response.set_cookie(
            'selected_cities',
            selected_cities_encoded,
            max_age=7 * 24 * 60 * 60,
        )
        return response
