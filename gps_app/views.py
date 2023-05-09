from django.shortcuts import render
from django.http import HttpResponse
from .models import GPSData

def receive_data(request):
    if request.method == 'POST':
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        GPSData.objects.create(latitude=latitude, longitude=longitude)
        return HttpResponse('Data received and stored.')
    else:
        return HttpResponse('Invalid request method.')

def show_data(request):
    gps_data = GPSData.objects.all()
    return render(request, 'gps_app/show_data.html', {'gps_data': gps_data})

