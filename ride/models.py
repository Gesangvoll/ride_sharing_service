from django.db import models
from login.models import User
from enum import Enum
# Create your models here.

class OwnerRequest(models.Model):
    owner_id = models.ForeignKey(User, on_delete=models.CASCADE, primary_key=True)
    is_open = models.BooleanField
    is_sharable = models.BooleanField
    is_confirmed = models.BooleanField
    is_completed = models.BooleanField
    destination = models.CharField(max_length=200)
    passenger_num = models.IntegerField
    order_date = models.DateField
    arrival_time = models.DateTimeField

class SharerRequest(models.Model):
    sharer_id = models.ForeignKey(OwnerRequest, on_delete=models.CASCADE, primary_key=True)
    earliest_time = models.DateTimeField
    latest_time = models.DateTimeField
    passenger_num = models.IntegerField


class Vehicle(models.Model):
    class Type(Enum):
        SEDAN = 'sedan'
        SUV = 'suv'
        COUPE = 'coupe'
        VAN = 'van'
        HYPER = 'hyper'

    plate_number = models.ForeignKey(User, on_delete=models.CASCADE, primary_key=True)
    type = models.CharField(max_length=6, choices=[(type, type.value) for type in Type])


