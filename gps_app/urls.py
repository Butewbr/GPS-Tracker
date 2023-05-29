from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('/login', views.login, name='login'),
    path('/profile', views.profile, name='profile'),
    path('/register', views.register, name='register'),
    path('/table', views.table, name='table'),
]
