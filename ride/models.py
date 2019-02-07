from django.db import models
from login.models import User
from django.utils import timezone
from model_utils import Choices
# Create your models here.

STATUS = Choices('open', 'shared','confirmed', 'completed')
TYPE = Choices('sedan', 'suv', 'coupe', 'van', 'hyper')


class OwnerRequest(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner_owner_request_set')
    is_sharable = models.BooleanField(default=False, blank=False)
    status = models.CharField( max_length=10, choices=STATUS, default='open')
    destination = models.CharField(max_length=200)
    passenger_num = models.IntegerField(default=1)
    total_passenger = models.IntegerField(default=1)
    vehicle_type = models.CharField(max_length=6, choices=TYPE, default='sedan')
    driver = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    created_date = models.DateTimeField('Create Date', default=timezone.now)
    arrival_time = models.DateTimeField(blank=True, null=True, default=timezone.now())
    special_vehicle_info = models.TextField(blank=True, null=True)


class SharerRequest(models.Model):
    sharer = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    owner_request = models.ForeignKey(OwnerRequest, on_delete=models.CASCADE)
    destination = models.CharField(max_length=200)
    earliest_time = models.DateTimeField(blank=True, null=True, default=timezone.now())
    created_date = models.DateTimeField('Create Date', default=timezone.now)
    latest_time = models.DateTimeField(blank=True, null=True, default=timezone.now())
    passenger_num = models.IntegerField(default=1)
    vehicle_type = models.CharField(max_length=6, choices=TYPE)


class Vehicle(models.Model):
    plate_number = models.CharField(max_length=10, blank=False, null=False)
    driver = models.OneToOneField(User, on_delete=models.CASCADE, blank=False, null=False)
    volume = models.IntegerField(null=False, blank=False)
    vehicle_type = models.CharField(max_length=6, choices=TYPE, blank=False, null=False)
    special_vehicle_info = models.TextField(blank=True, null=True)


