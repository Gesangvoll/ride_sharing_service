from django.db import models
from django.contrib.auth.models import AbstractUser
from enum import Enum
# Create your models here.


class User(AbstractUser):
    class Roles(Enum):
        OW = 'owner'
        DR = 'driver'
        SH = 'sharer'

    catalog = models.CharField(max_length=6, choices=[(catalog, catalog.value) for catalog in Roles])
    plate_number = models.CharField(max_length=10, blank=True)
