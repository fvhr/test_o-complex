import urllib

import rest_framework
import rest_framework.viewsets

from geo.models import City
from geoAPI.serializers import (
    CitySerializer,
    CityCountSerializer,
    CityQuerySerializer,
)


class CitiesViewSet(rest_framework.viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer


class CitySearchView(rest_framework.views.APIView):
    def get(self, request, *args, **kwargs):
        city = request.query_params.get('city', None)
        if city is not None:
            city = urllib.parse.unquote(city)
            cities = City.objects.filter(name__icontains=city)
            serializer = CityQuerySerializer(cities, many=True)
            return rest_framework.response.Response(
                serializer.data,
                status=rest_framework.status.HTTP_200_OK,
            )
        return rest_framework.response.Response(
            {'error': 'Query parameter is required'},
            status=rest_framework.status.HTTP_400_BAD_REQUEST,
        )


class CityCountView(rest_framework.views.APIView):
    def get(self, request, *args, **kwargs):
        cities = City.objects.filter(request_count__gt=0)
        serializer = CityCountSerializer(cities, many=True)
        return rest_framework.response.Response(
            serializer.data,
            status=rest_framework.status.HTTP_200_OK,
        )
