from django.contrib import admin
import django.urls
from django.views.generic import RedirectView

import geo.urls
from rest_framework import routers

from geoAPI.views import CitiesViewSet, CitySearchView, CityCountView

router = routers.SimpleRouter()
router.register(r'cities', CitiesViewSet)

urlpatterns = [
    django.urls.path('admin/', admin.site.urls),
    django.urls.path(
        '',
        RedirectView.as_view(url='/geo/auto', permanent=True),
        name='home-redirect',
    ),
    django.urls.path(
        'geo/',
        django.urls.include(geo.urls, 'geo'),
    ),
    django.urls.path('api/v1/', django.urls.include(router.urls)),
    django.urls.path(
        'api/v1/found_city/', CitySearchView.as_view(), name='city-search',
    ),
    django.urls.path(
        'api/v1/count_cities/', CityCountView.as_view(), name='city-count',
    ),
]
