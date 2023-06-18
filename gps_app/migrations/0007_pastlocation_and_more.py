# Generated by Django 4.2.2 on 2023-06-18 17:12

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gps_app', '0006_remove_gpsdevice_name_remove_gpsdevice_user_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='PastLocation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latitude', models.DecimalField(decimal_places=6, max_digits=9)),
                ('longitude', models.DecimalField(decimal_places=6, max_digits=9)),
                ('timestamp', models.DateTimeField(default=datetime.datetime.now)),
            ],
        ),
        migrations.RenameField(
            model_name='gpsdevice',
            old_name='latitude',
            new_name='current_latitude',
        ),
        migrations.RenameField(
            model_name='gpsdevice',
            old_name='longitude',
            new_name='current_longitude',
        ),
        migrations.AddField(
            model_name='gpsdevice',
            name='name',
            field=models.CharField(default='BernardoLegal', max_length=100),
        ),
    ]
