from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('api/places/', views.api_places, name='api_places'),
    path('map', views.map_page, name='map'),
    path('my-day', views.my_day, name='my_day'),
    path('place/<slug:slug>/', views.place_detail, name='place_detail'),
]

