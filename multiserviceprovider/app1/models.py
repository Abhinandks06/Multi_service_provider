from django.db import models
from django.contrib.auth.models import AbstractUser

class MyUser(AbstractUser):
    email = models.EmailField(unique=True)  # Add email field with unique constraint
    dob = models.DateField(null=True, blank=True)
    password = models.CharField(max_length=128, default="")
    phone = models.CharField(max_length=12, default="", unique=True)  # Set as unique
    district = models.TextField(max_length=100, default="")
    state = models.TextField(max_length=100, default="")
    role = models.CharField(max_length=15, default='')

