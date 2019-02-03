from django.db import models
from login.models import User
from enum import Enum
from django.utils import timezone
# Create your models here.

class OrderStatus(Enum):
    OP = 'open'
    CON = 'confirmed'
    COM = 'completed'

class OwnerRequest(models.Model):

    owner_id = models.ForeignKey(User, on_delete=models.CASCADE)
    is_sharable = models.BooleanField
    status = models.CharField( max_length=10, choices=[(status, status.value) for status in OrderStatus])
    destination = models.CharField(max_length=200)
    passenger_num = models.IntegerField(default=1)
    total_passenger = models.IntegerField(default=1)
    created_date = models.DateTimeField('Create Date', default=timezone.now)
    arrival_time = models.DateTimeField(blank=True, null=True)


class SharerRequest(models.Model):
    sharer_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    owner_request_id = models.ForeignKey(OwnerRequest, on_delete=models.CASCADE)
    earliest_time = models.DateTimeField(blank=True, null=True)
    created_date = models.DateTimeField('Create Date', default=timezone.now)
    latest_time = models.DateTimeField(blank=True, null=True)
    passenger_num = models.IntegerField(default=1)


class VehicleType(Enum):
    SE = 'sedan'
    SUV = 'suv'
    CO = 'coupe'
    VA = 'van'
    HY = 'hyper'


class Vehicle(models.Model):
    plate_number = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    type = models.CharField(max_length=6, choices=[(type, type.value) for type in VehicleType])


