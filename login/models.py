from django.db import models
from django.contrib.auth.models import AbstractUser
from model_utils import Choices

# Create your models here.


class User(AbstractUser):
    ROLE = Choices('owner', 'driver', 'sharer')
    catalog = models.CharField(max_length=6, choices=ROLE, blank=True, null=True)
    plate_number = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return self.username