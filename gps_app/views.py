from django.shortcuts import render
from django.http import HttpResponse
from .models import User, GPSDevice, Movement

def home(request):
    return render(request, 'index.html')

def receive_data(request):
    if request.method == 'POST':
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        GPSDevice.objects.create(latitude=latitude, longitude=longitude)
        return HttpResponse('Data received and stored.')
    else:
        return HttpResponse('Invalid request method.')

def show_data(request):
    gps_devices = GPSDevice.objects.all()
    return render(request, 'show_data.html', {'gps_data': gps_devices})

