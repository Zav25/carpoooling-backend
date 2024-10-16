from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(username, email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    email = models.EmailField(unique=True)

    is_driver = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=15, unique=True, default="")
    nid_passport = models.CharField(max_length=100, unique=True, default="")
    address = models.TextField(default="")

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', 'phone_number', 'nid_passport', 'address']

    def __str__(self):
        return self.username




class Vehicle(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    license_plate = models.CharField(max_length=10)
    model = models.CharField(max_length=50)
    capacity = models.IntegerField(default=4)

class Ride(models.Model):
    driver = models.ForeignKey(User, related_name='driver_rides', null=True, on_delete=models.SET_NULL)
    passenger = models.ForeignKey(User, related_name='passenger_rides', null=True, blank=True, on_delete=models.SET_NULL)    
    origin = models.CharField(max_length=255, null=True)
    destination = models.CharField(max_length=255, null=True)
    num_persons = models.PositiveIntegerField(null=True)  # Number of persons for the ride
    start_time = models.DateTimeField(null=True)  # Start time for the ride
    end_time = models.DateTimeField(null=True)  # End time for the ride
    price = models.DecimalField(max_digits=6, decimal_places=2, null=True)  # Price of the ride

    def __str__(self):
        return f"Ride from {self.origin} to {self.destination} with {self.num_persons} persons"
