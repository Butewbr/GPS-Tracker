# Generated by Django 4.2.2 on 2023-06-18 16:00

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gps_app', '0003_gpsdevice_is_connected'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gpsdevice',
            name='is_connected',
        ),
        migrations.AddField(
            model_name='gpsdevice',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]