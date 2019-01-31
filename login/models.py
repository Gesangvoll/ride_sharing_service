from django.db import models
from django.contrib.auth.models import AbstractUser
from enum import Enum
# Create your models here.

class Roles(Enum):
    OW = 'owner'
    DR = 'driver'
    SH = 'sharer'


class User(AbstractUser):
    catalog = models.CharField(max_length=6, choices=[(tag, tag.value) for tag in Roles], blank=True, null=True)
    plate_number = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return self.username

    