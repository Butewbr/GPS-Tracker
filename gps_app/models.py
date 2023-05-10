from django.db import models

class User(models.Model):
    id = models.IntegerField(auto_created=True, primary_key=True)
    password = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)

class GPSDevice(models.Model):
    id = models.IntegerField(auto_created=True, primary_key=True)
    name = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    is_connected = models.BooleanField(default=False)

class Movement(models.Model):
    id = models.IntegerField(auto_created=True, primary_key=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    device_id = models.ForeignKey(GPSDevice, on_delete=models.CASCADE)
