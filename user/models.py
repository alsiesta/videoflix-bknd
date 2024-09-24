from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
       story = models.CharField(max_length=100, blank=True, null=True, default='')
       phone = models.CharField(max_length=36, blank=True, null=True, default='')
       address = models.CharField(max_length=200, blank=True, null=True, default='')
