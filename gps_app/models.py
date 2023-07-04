from django.db import models
from datetime import datetime

class User(models.Model):
    password = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)

class Cercado(models.Model):
    name = models.CharField(max_length=100, default='Nameless Cercado')
    lat1 = models.DecimalField(max_digits=9, decimal_places=3)
    lon1 = models.DecimalField(max_digits=9, decimal_places=3)
    lat2 = models.DecimalField(max_digits=9, decimal_places=3)
    lon2 = models.DecimalField(max_digits=9, decimal_places=3)
    lat3 = models.DecimalField(max_digits=9, decimal_places=3)
    lon3 = models.DecimalField(max_digits=9, decimal_places=3)
    lat4 = models.DecimalField(max_digits=9, decimal_places=3)
    lon4 = models.DecimalField(max_digits=9, decimal_places=3)

class GPSDevice(models.Model):
    name = models.CharField(max_length=100, default='Nameless GPS')
    current_latitude = models.DecimalField(max_digits=9, decimal_places=6)
    current_longitude = models.DecimalField(max_digits=9, decimal_places=6)
    current_altitude = models.DecimalField(max_digits=9, decimal_places=3)
    current_speed = models.DecimalField(max_digits=9, decimal_places=3)
    last_updated = models.DateTimeField(default=datetime.now)
    cercado = models.ForeignKey(Cercado, on_delete=models.SET_NULL, null=True)

class PreviousLocation(models.Model):
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    timestamp = models.DateTimeField(default=datetime.now)
    device_id = models.ForeignKey(GPSDevice, on_delete=models.CASCADE)


class Movement(models.Model):
    first_location = models.ForeignKey(PreviousLocation, on_delete=models.CASCADE)
    final_latitude = models.DecimalField(max_digits=9, decimal_places=6)
    final_longitude = models.DecimalField(max_digits=9, decimal_places=6)
    start_time = models.DateTimeField(auto_now_add=True)
    finish_time = models.DateTimeField(auto_now_add=True)
    device_id = models.ForeignKey(GPSDevice, on_delete=models.CASCADE)
    