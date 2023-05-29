from django.shortcuts import render
from django.http import HttpResponse
from .models import User, GPSDevice, Movement

def home(request):
    return render(request, 'index.html')

def login(request):
    return render(request, 'login.html')

def profile(request):
    return render(request, 'profile.html')

def register(request):
    return render(request, 'register.html')

def table(request):
    return render(request, 'table.html')

