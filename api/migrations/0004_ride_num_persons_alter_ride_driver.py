# Generated by Django 5.1.1 on 2024-10-16 17:05

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_remove_ride_available_seats_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='ride',
            name='num_persons',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='ride',
            name='driver',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='driver_rides', to=settings.AUTH_USER_MODEL),
        ),
    ]
