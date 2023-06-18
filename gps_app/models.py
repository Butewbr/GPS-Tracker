from django.db import models
from datetime import datetime

class User(models.Model):
    password = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)

class GPSDevice(models.Model):
    name = models.CharField(max_length=100, default='BernardoLegal')
    current_latitude = models.DecimalField(max_digits=9, decimal_places=6)
    current_longitude = models.DecimalField(max_digits=9, decimal_places=6)
    timestamp = models.DateTimeField(default=datetime.now)
    # user_id = models.ForeignKey(User, on_delete=models.CASCADE)

class PastLocation(models.Model):
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    timestamp = models.DateTimeField(default=datetime.now)


class Movement(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    device_id = models.ForeignKey(GPSDevice, on_delete=models.CASCADE)
