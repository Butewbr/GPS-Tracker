from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import User, GPSDevice, Movement, PastLocation
from rest_framework.decorators import api_view
from rest_framework.response import Response

def home(request):
    try:
        gps_data = GPSDevice.objects.get(name='Nameless GPS')
    except:
        nothing_found={'name': 'nothingfound', 'current_latitude':0, 'current_longitude':0}
        
        return render(request, 'index.html', {'gps_data': nothing_found})

    return render(request, 'index.html', {'gps_data': gps_data})

def login(request):
    return render(request, 'login.html')

def profile(request):
    return render(request, 'profile.html')

def register(request):
    return render(request, 'register.html')

def table(request):
    return render(request, 'table.html')

@api_view(['POST'])
def gps_coordinates(request):
    name = 'Nameless GPS'
    latitude = request.data.get('latitude')
    longitude = request.data.get("longitude")
    altitude = request.data.get('altitude')
    speed = request.data.get('speed')
    counter = request.data.get('counter')

    # margem de erro do gps
    if speed < 0.99:
        speed = 0

    print(latitude)
    print(longitude)

    print(counter)

    print('Counter % 10 = 0? '+str(counter%10 is 0)+' it is '+str(counter%10))

    try:
        gps_data = GPSDevice.objects.get(name=name)

        print("Updating GPSDevice's data...")

        if counter+1 % 10 == 0:
            new_past_location = PastLocation(latitute = latitude, longitude = longitude, timestamp = gps_data.last_updated, device_id = gps_data.id)
            print('New past location added to database.')

        gps_data.current_latitude = latitude
        gps_data.current_longitude = longitude
        gps_data.current_altitude = altitude
        gps_data.current_speed = speed
    except:
        gps_data = GPSDevice(name=name, current_latitude=latitude, current_longitude=longitude, current_altitude=altitude, current_speed=speed)
        print("New GPSDevice saved into database!")

    
    gps_data.save()

    return Response({'message': 'GPS coordinates saved'})

def gps_data_list(request):
    try:
        gps_data = GPSDevice.objects.get(name='Nameless GPS')
    except:
        nothing_found={'name': 'nothingfound', 'current_latitude':0, 'current_longitude':0}
        return render(request, 'index.html', {'gps_data': nothing_found})
        
    return render(request, 'gps_data_list.html', {'gps_data': gps_data})