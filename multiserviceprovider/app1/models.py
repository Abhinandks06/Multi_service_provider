from django.db import models
from django.contrib.auth.models import AbstractUser

class MyUser(AbstractUser):
    email = models.EmailField(unique=True)  # Add email field with unique constraint
    password = models.CharField(max_length=128, default="")
    role = models.CharField(max_length=15, default='')
class ServiceProvider(models.Model):
    providername = models.CharField(max_length=100)
    ownername = models.CharField(max_length=100)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=50)
    service_type = models.CharField(max_length=100)
class Client(models.Model):
    first_name=models.TextField(max_length=100)
    last_name=models.TextField(max_length=100)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)  # Add email field with unique constraint
    dob = models.DateField(null=True, blank=True)
    password = models.CharField(max_length=128)
    phone = models.CharField(max_length=12, unique=True)  # Set as unique
    district = models.TextField(max_length=100)
    state = models.TextField(max_length=100)
    role = models.CharField(max_length=15, default='')
class Worker(models.Model):
    first_name=models.TextField(max_length=100)
    last_name=models.TextField(max_length=100)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)  # Add email field with unique constraint
    dob = models.DateField(null=True, blank=True)
    password = models.CharField(max_length=128)
    phone = models.CharField(max_length=12, unique=True)  # Set as unique
    district = models.TextField(max_length=100)
    state = models.TextField(max_length=100)
    role = models.CharField(max_length=15, default='')
    provider= models.CharField(max_length=50)

    