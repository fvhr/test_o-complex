from django.urls import path

from . import views

app_name = 'geo'

urlpatterns = [
    path('auto/', views.GeoView.as_view(), name='geo-auto'),
    path('<int:pk>/', views.GeoDetailView.as_view(), name='geo-detail'),
]
