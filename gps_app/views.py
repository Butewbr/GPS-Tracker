from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from datetime import date, time, datetime
from .models import User, GPSDevice, Movement, PreviousLocation, Cercado
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.gis.geos import Point
import json


def is_inside(gps_device):
    lat = gps_device.current_latitude
    lon = gps_device.current_longitude

    cercado  = gps_device.cercado

    # Check if the GPS device is inside the cercado polygon
    num_points = 4
    inside = False

    for i in range(num_points):
        j = (i + 1) % num_points

        # Extract the latitude and longitude coordinates of each vertex
        lat_i, lon_i = getattr(cercado, f'lat{i+1}'), getattr(cercado, f'lon{i+1}')
        lat_j, lon_j = getattr(cercado, f'lat{j+1}'), getattr(cercado, f'lon{j+1}')

        if (
            ((lat_i > lat) != (lat_j > lat)) and
            (lon < (lon_j - lon_i) * (lat - lat_i) / (lat_j - lat_i) + lon_i)
        ):
            inside = not inside

    return inside


def home(request):
    notify = False
    inside = True
    try:
        gps_data = GPSDevice.objects.get(id=1)
    except:
        nothing_found={'name': 'nothingfound', 'current_latitude':0, 'current_longitude':0}
        
        return render(request, 'index.html', {'gps_data': nothing_found})

    total_distance = 0
    previous_point = None

    today = date.today()

    coordinates = PreviousLocation.objects.filter(
        Q(timestamp__year=today.year) &
        Q(timestamp__month=today.month) &
        Q(timestamp__day=today.day)).order_by('timestamp')

    for coordinate in coordinates:
        current_point = Point(float(coordinate.longitude), float(coordinate.latitude))

        if previous_point:
            distance = previous_point.distance(current_point)
            total_distance += distance

        previous_point = current_point

    month_distance = 0
    previous_point = None

    month_coordinates = PreviousLocation.objects.filter(
        Q(timestamp__year=today.year) &
        Q(timestamp__month=today.month) &
        Q(timestamp__day=today.day)).order_by('timestamp')

    for coordinate in month_coordinates:
        current_point = Point(float(coordinate.longitude), float(coordinate.latitude))

        if previous_point:
            distance = previous_point.distance(current_point)
            month_distance += distance

        previous_point = current_point

    print('Distance today: '+str(total_distance))
    print('Distance this month: '+str(month_distance))
    
    if gps_data.cercado:
        print("Cercado: ")
        print(gps_data.cercado)


    movements = Movement.objects.filter(
        Q(start_time__year=today.year) &
        Q(start_time__month=today.month) &
        Q(start_time__day=today.day)).order_by('start_time')

    # graph values:

    distances_today = []
    i = 0
    while i < 22:
        start_time = time(i, 0)
        if i+3 == 24:
            end_time = time(i+2, 0)
        else:
            end_time = time(i+3, 0)

        start_datetime = datetime.combine(today, start_time)
        end_datetime = datetime.combine(today, end_time)

        current_coordinates = PreviousLocation.objects.filter(
            Q(timestamp__gte=start_datetime) &
            Q(timestamp__lt=end_datetime)).order_by('timestamp')
        
        this_period_distance = 0

        if current_coordinates:        
            current_distance = 0

            for coordinate in current_coordinates:
                current_point = Point(float(coordinate.longitude), float(coordinate.latitude))

                if previous_point:
                    current_distance = previous_point.distance(current_point)
                    this_period_distance += current_distance

                previous_point = current_point

        distances_today.append(float(this_period_distance))

        i += 3
    
    print('Distance per 3 hour: '+str(distances_today))

    chart_labels = ["00:00", "03:00", "06:00", "09:00", "12:00", "15:00", "18:00", "21:00"]
    chart_data = {
        "type": "line",
        "data": {
            "labels": chart_labels,
            "datasets": [{
                "label": "Earnings",
                "fill": True,
                "data": distances_today,
                "backgroundColor": "rgba(78, 115, 223, 0.05)",
                "borderColor": "rgba(78, 115, 223, 1)"
            }]
        },
        "options": {
            "maintainAspectRatio": False,
            "legend": {
                "display": False,
                "labels": {
                    "fontStyle": "normal"
                }
            },
            "title": {
                "fontStyle": "normal"
            },
            "scales": {
                "xAxes": [{
                    "gridLines": {
                        "color": "rgb(234, 236, 244)",
                        "zeroLineColor": "rgb(234, 236, 244)",
                        "drawBorder": False,
                        "drawTicks": False,
                        "borderDash": ["2"],
                        "zeroLineBorderDash": ["2"],
                        "drawOnChartArea": False
                    },
                    "ticks": {
                        "fontColor": "#858796",
                        "fontStyle": "normal",
                        "padding": 20
                    }
                }],
                "yAxes": [{
                    "gridLines": {
                        "color": "rgb(234, 236, 244)",
                        "zeroLineColor": "rgb(234, 236, 244)",
                        "drawBorder": False,
                        "drawTicks": False,
                        "borderDash": ["2"],
                        "zeroLineBorderDash": ["2"]
                    },
                    "ticks": {
                        "fontColor": "#858796",
                        "fontStyle": "normal",
                        "padding": 20
                    }
                }]
            }
        }
    }

    chart_data_json = json.dumps(chart_data)

    if gps_data.current_speed > 5:
        notify = True

    if gps_data.cercado:
        inside = is_inside(gps_data)

    todays_day = datetime.today().day

    avg_distance = month_distance/todays_day

    return render(request, 'index.html', {'gps_data': 
    gps_data, 'todays_distance': total_distance, 'months_distance': month_distance, 'gps_locations_today': coordinates, 'total_movements': len(movements), 'distance_per_time': distances_today, 'chart_data': chart_data_json, 'notify': notify, 'avg_distance': avg_distance, 'inside': inside})

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

    print('Counter % 10 = 0? '+str(counter%10 == 0)+' it is '+str(counter%10))

    try:
        gps_data = GPSDevice.objects.get(id=1)
        print("Updating GPSDevice's data...")
        # Every 10 new received information, a new data of location is saved.
        if counter % 10 == 0:
            try:
                new_past_location = PreviousLocation(latitude = latitude, longitude = longitude, timestamp = gps_data.last_updated, device_id = gps_data)
                new_past_location.save()
                print('New past location added to database.')
            except Exception as e:
                print(e)
                print("Could not register previous location.")
    except:
        gps_data = GPSDevice(name='Nameless GPS', current_latitude=latitude, current_longitude=longitude, current_altitude=altitude, current_speed=speed)
        print("Device Not Found. Creating new on Database.")
        
    today = date.today()
    current_point = Point(float(longitude), float(latitude))

    coordinates = PreviousLocation.objects.filter(
        Q(timestamp__year=today.year) &
        Q(timestamp__month=today.month) &
        Q(timestamp__day=today.day)).order_by('timestamp')

    if coordinates:
        distance_traveled = current_point.distance(Point(float(coordinates[0].longitude), float(coordinates[0].latitude)))
        print('Distance from last time: '+str(distance_traveled))
        if distance_traveled > 0.5 and speed >= 1:
            print('MOVEMENT DETECTED')
            new_movement = Movement(device_id=gps_data.id, first_location=coordinates[0], final_latitude=latitude, final_longitude=longitude, start_time=coordinates[0].timestamp, finish_time=date.today())
            new_movement.save()    

    gps_data.current_latitude = latitude
    gps_data.current_longitude = longitude
    gps_data.current_altitude = altitude
    gps_data.current_speed = speed

    gps_data.save()

    return Response({'message': 'GPS coordinates saved'})

def gps_data_list(request):
    try:
        gps_data = GPSDevice.objects.get(id=1)
    except:
        nothing_found={'name': 'nothingfound', 'current_latitude':0, 'current_longitude':0}
        return render(request, 'index.html', {'gps_data': nothing_found})
        
    return render(request, 'gps_data_list.html', {'gps_data': gps_data})

def update_device_name(request):
    device = GPSDevice.objects.get(id=1)
    new_name = request.POST.get('name')

    device.name = new_name
    device.save()

    return redirect('/')

def config_cercado(request):
    device = GPSDevice.objects.get(id=1)

    name = request.POST.get('name')

    lat1 = float(request.POST.get('lat1'))
    lon1 = float(request.POST.get('lon1'))

    lat2 = float(request.POST.get('lat2'))
    lon2 = float(request.POST.get('lon2'))
    
    lat3 = float(request.POST.get('lat3'))
    lon3 = float(request.POST.get('lon3'))
    
    lat4 = float(request.POST.get('lat4'))
    lon4 = float(request.POST.get('lon4'))

    cercado_data = Cercado(name=name, lat1=lat1, lon1=lon1, lat2=lat2, lon2=lon2, lat3=lat3, lon3=lon3, lat4=lat4, lon4=lon4)

    cercado_data.save()

    device.cercado = cercado_data
    
    device.save()

    return redirect('/')

def remove_cercado(request):
    gps_device = GPSDevice.objects.get(id=1)

    # Remove the cercado association by setting it to None
    gps_device.cercado = None
    gps_device.save()

    return redirect('/')


def example(request):
    gps_data = {'name': "The Example GPS", 'current_latitude': -28.949480733, 'current_longitude': -49.466650288, 'current_altitude': 15.4785, 'current_speed': 0.0}

    notify = False

    distances_today = [0.0, 0.0, 4.5, 1.3, 5.2, 1.2, 3.3, 0.7]

    movements = 4

    month_distance = 128.22

    todays_day = datetime.today().day

    avg_distance = month_distance/todays_day

    total_distance = 0
    for distance in distances_today:
        total_distance += distance
    
    print('Distance per 3 hour: '+str(distances_today))

    chart_labels = ["00:00", "03:00", "06:00", "09:00", "12:00", "15:00", "18:00", "21:00"]
    chart_data = {
        "type": "line",
        "data": {
            "labels": chart_labels,
            "datasets": [{
                "label": "Earnings",
                "fill": True,
                "data": distances_today,
                "backgroundColor": "rgba(78, 115, 223, 0.05)",
                "borderColor": "rgba(78, 115, 223, 1)"
            }]
        },
        "options": {
            "maintainAspectRatio": False,
            "legend": {
                "display": False,
                "labels": {
                    "fontStyle": "normal"
                }
            },
            "title": {
                "fontStyle": "normal"
            },
            "scales": {
                "xAxes": [{
                    "gridLines": {
                        "color": "rgb(234, 236, 244)",
                        "zeroLineColor": "rgb(234, 236, 244)",
                        "drawBorder": False,
                        "drawTicks": False,
                        "borderDash": ["2"],
                        "zeroLineBorderDash": ["2"],
                        "drawOnChartArea": False
                    },
                    "ticks": {
                        "fontColor": "#858796",
                        "fontStyle": "normal",
                        "padding": 20
                    }
                }],
                "yAxes": [{
                    "gridLines": {
                        "color": "rgb(234, 236, 244)",
                        "zeroLineColor": "rgb(234, 236, 244)",
                        "drawBorder": False,
                        "drawTicks": False,
                        "borderDash": ["2"],
                        "zeroLineBorderDash": ["2"]
                    },
                    "ticks": {
                        "fontColor": "#858796",
                        "fontStyle": "normal",
                        "padding": 20
                    }
                }]
            }
        }
    }

    if gps_data['current_speed'] > 1:
        notify = True

    chart_data_json = json.dumps(chart_data)

    return render(request, 'example.html', {'gps_data': 
    gps_data, 'todays_distance': total_distance, 'months_distance': month_distance, 'total_movements': movements, 'distance_per_time': distances_today, 'chart_data': chart_data_json, 'notify': notify, 'avg_distance': avg_distance})