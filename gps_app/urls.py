from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('profile/', views.profile, name='profile'),
    path('register/', views.register, name='register'),
    path('table/', views.table, name='table'),
    path('api/coordinates', views.gps_coordinates, name='gps_coordinates'),
    path('gps-data/', views.gps_data_list, name='gps_data_list'),
]
