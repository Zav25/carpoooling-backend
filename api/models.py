from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class User(AbstractUser):
    is_driver = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=15)

    # Add related_name arguments to avoid conflicts
    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',  # Change related_name to avoid conflict
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_permissions_set',  # Change related_name to avoid conflict
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )


class Vehicle(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    license_plate = models.CharField(max_length=10)
    model = models.CharField(max_length=50)
    capacity = models.IntegerField(default=4)

class Ride(models.Model):
    driver = models.ForeignKey(User, related_name='driver_rides', on_delete=models.CASCADE)
    origin = models.CharField(max_length=255)
    destination = models.CharField(max_length=255)
    departure_time = models.DateTimeField()
    available_seats = models.IntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
