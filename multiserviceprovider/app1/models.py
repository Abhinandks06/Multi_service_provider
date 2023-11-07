from django.db import models
from django.contrib.auth.models import AbstractUser

class MyUser(AbstractUser):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128, default="")
    role = models.CharField(max_length=15, default='client')
    userid = models.AutoField(primary_key=True) 
    
class ServiceProvider(models.Model):
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE,primary_key=True)
    providername = models.CharField(max_length=100, unique=True)
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
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE,primary_key=True)
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
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE,primary_key=True)
    provider = models.TextField(max_length=100)
    # Additional fields specific to workers can be added here
    first_name = models.TextField(max_length=100)
    last_name = models.TextField(max_length=100)
    email = models.EmailField(unique=True)
    dob = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=12, unique=True)
    district = models.TextField(max_length=100)
    state = models.TextField(max_length=100)
    role = models.CharField(max_length=15)
class ClientBooking(models.Model):
    PENDING = 'pending'
    APPROVED = 'approved'
    CANCELED = 'canceled'
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (APPROVED, 'Approved'),
        (CANCELED, 'Canceled'),
    ]
    bookingid = models.AutoField(primary_key=True)
    clientid = models.ForeignKey('Client', on_delete=models.CASCADE)
    providerid = models.ForeignKey('ServiceProvider', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PENDING)

class WorkerStatus(models.Model):
    providerid = models.ForeignKey('ServiceProvider', on_delete=models.CASCADE)
    workerid = models.ForeignKey('Worker', on_delete=models.CASCADE)
    
    # Choices for work status
    PENDING = 'pending'
    IN_PROGRESS = 'in_progress'
    COMPLETED = 'completed'
    WORK_STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (IN_PROGRESS, 'In Progress'),
        (COMPLETED, 'Completed'),
    ]
    
    workstatus = models.CharField(max_length=15, choices=WORK_STATUS_CHOICES, default=PENDING)


    