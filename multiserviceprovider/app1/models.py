from django.db import models
from django.contrib.auth.models import AbstractUser

class MyUser(AbstractUser):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128, default="")
    role = models.CharField(max_length=15, default='client')
    userid = models.AutoField(primary_key=True) 
class ServiceTypes(models.Model):
    service_id = models.AutoField(primary_key=True)
    service_type = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    number_of_providers = models.IntegerField(default=0) 

class ServiceProvider(models.Model):
    providerid = models.AutoField(primary_key=True)  # Auto-incremented primary key
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE, unique=True)
    providername = models.CharField(max_length=100, unique=True)
    ownername = models.CharField(max_length=100)
    username = models.CharField(max_length=50, unique=True)
    state = models.CharField(max_length=100)
    district = models.CharField(max_length=100,default="kottayam")
    contact_number = models.CharField(max_length=15)
    service_type = models.ManyToManyField(ServiceTypes)

class BranchManager(models.Model):
    managerid = models.AutoField(primary_key=True)
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE, unique=True)
    providerid = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE)
    providername = models.CharField(max_length=100)
    date_of_joining = models.DateField()
    phone_no = models.CharField(max_length=15)
    state = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    pincode = models.IntegerField()
    email = models.EmailField(unique=True)
    
class Branch(models.Model):
    branchid = models.AutoField(primary_key=True)
    providerid = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE)
    providername = models.CharField(max_length=100)
    service_type = models.ForeignKey(ServiceTypes, on_delete=models.CASCADE)
    district = models.CharField(max_length=100)
    pincode = models.IntegerField()
    status = models.CharField(max_length=10, default='inactive')
class BranchManagerAssignment(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    manager = models.ForeignKey(BranchManager, on_delete=models.CASCADE)    
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
    pincode = models.IntegerField()
    role = models.CharField(max_length=15, default='')

class Worker(models.Model):
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE, primary_key=True)
    provider = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE)
    branchid = models.ManyToManyField(Branch)
    service_types = models.ManyToManyField(ServiceTypes)
    first_name = models.TextField(max_length=100)
    last_name = models.TextField(max_length=100)
    email = models.EmailField(unique=True)
    dob = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=12, unique=True)
    pincode = models.IntegerField()
    district = models.TextField(max_length=100)
    state = models.TextField(max_length=100)
    role = models.CharField(max_length=15)
    status = models.CharField(max_length=15)

class ClientBooking(models.Model):
    PENDING = 'pending'
    APPROVED = 'approved'
    CANCELED = 'canceled'
    COMPLETED = 'completed'
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (APPROVED, 'Approved'),
        (CANCELED, 'Canceled'),
        (COMPLETED, 'Completed'),
    ]

    bookingid = models.AutoField(primary_key=True)
    clientid = models.ForeignKey('Client', on_delete=models.CASCADE)
    district = models.TextField(max_length=100)
    branchid = models.ForeignKey('Branch', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PENDING)

class WorkerStatus(models.Model):
    branchid = models.ForeignKey('Branch', on_delete=models.CASCADE)
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
class Service(models.Model):
    ASSIGNED = 'assigned'
    UNDERPROGRESS = 'underprogress'
    COMPLETED = 'completed'
    CANCELED = 'canceled'
    REPORTGIVEN = 'reportgiven'
    REPORTVERIFIED = 'reportverified'
    REQUESTED = 'requested'
    IN_PROGRESS = 'in_progress'
    COMPLETED = 'completed'
    CANCELED = 'canceled'
    STATUS_CHOICES = [
        (ASSIGNED, 'Assigned'),
        (UNDERPROGRESS, 'Underprogress'),
        (COMPLETED, 'Completed'),
        (CANCELED, 'Canceled'),
        (REPORTGIVEN, 'Report Given'),
        (REPORTVERIFIED, 'Report Verified'),
    ]
    PAYMENT_STATUS_CHOICES = [
        (REQUESTED, 'Requested'),
        (IN_PROGRESS, 'In Progress'),
        (COMPLETED, 'Completed'),

    ]
    serviceid = models.AutoField(primary_key=True)  # New field as primary key and autoincrement
    bookingid = models.ForeignKey('ClientBooking', on_delete=models.CASCADE)  # Foreign key to ClientBooking model
    clientid = models.ForeignKey('Client', on_delete=models.CASCADE)
    district = models.TextField(max_length=100)
    branchid = models.ForeignKey('Branch', on_delete=models.CASCADE)
    workerid = models.ManyToManyField('Worker')
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default=ASSIGNED)
    rating = models.IntegerField(blank=True, null=True)  # Field to store the rating
    review = models.TextField(blank=True, null=True) 
    reply= models.TextField(blank=True, null=True)
    paymentstatus = models.CharField(max_length=15, choices=PAYMENT_STATUS_CHOICES, default=REQUESTED)
class WorkerReport(models.Model):
    COMPLETED = 'completed'
    CANCELED = 'canceled'
    REPORTGIVEN = 'reportgiven'
    REPORTVERIFIED = 'reportverified'
    STATUS_CHOICES = [
        (COMPLETED, 'Completed'),
        (CANCELED, 'Canceled'),
        (REPORTGIVEN, 'ReportGiven'),
        (REPORTVERIFIED, 'ReportVerified'),
    ]
    reportid = models.AutoField(primary_key=True)
    serviceid = models.ForeignKey('Service', on_delete=models.CASCADE)
    user_id = models.ForeignKey('Worker', on_delete=models.CASCADE)
    branchid = models.ForeignKey('Branch', on_delete=models.CASCADE)
    duration_of_work = models.CharField(max_length=100)
    requirements = models.TextField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    num_workers_needed = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default=REPORTGIVEN)
    report_pdf = models.FileField(upload_to='worker_reports/', blank=True, null=True)

class WorkerLeaveapplication(models.Model):
    leaveid = models.AutoField(primary_key=True)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='worker_leave')
    LEAVE_TYPES = (
        ('medical', 'Medical'),
        ('family_emergency', 'FamilyEmergency'),
        ('other', 'Other'),
    )
    leavetype = models.CharField(max_length=20, choices=LEAVE_TYPES)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, default='pending')

class MultiBranch(models.Model):
    branchid = models.AutoField(primary_key=True)
    providerid = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE)
    providername = models.CharField(max_length=100)
    service_type = models.ForeignKey(ServiceTypes, on_delete=models.CASCADE)
    district = models.CharField(max_length=100)
    status = models.CharField(max_length=10, default='inactive')

class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()
    category = models.CharField(max_length=50)
    def __str__(self):
        return f"{self.category} - {self.question}"
    
class Salary(models.Model):
    salaryid = models.AutoField(primary_key=True)
    userid = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    branchid = models.ForeignKey(Branch, on_delete=models.CASCADE)
    date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=15, default='pending')

    def __str__(self):
        return f"Salary - {self.userid.username} - {self.date}"

class SalaryHistory(models.Model):
    historyid = models.AutoField(primary_key=True)
    salary = models.ForeignKey(Salary, on_delete=models.CASCADE)
    userid = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Salary History - {self.salary.userid.username} - {self.date}"
    

class ClientWorkRequest(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, null=False, blank=False)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True, blank=True)
    provider = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE, null=True, blank=True)
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE, null=True, blank=True)
    service_type = models.CharField(max_length=255)
    description = models.TextField()  # Renamed from 'details'
    district = models.CharField(max_length=100)
    status = models.CharField(max_length=10, default='pending')
    additional_info = models.TextField()
    start_date = models.DateField()  # Changed to DateField for start date
    end_date = models.DateField()    # Changed to DateField for end date

class Assignment(models.Model):
    requestid = models.ForeignKey(ClientWorkRequest, on_delete=models.CASCADE)
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, default='requested')

class Bonus(models.Model):
    bonusid = models.AutoField(primary_key=True)
    userid = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    reportid = models.ForeignKey(WorkerReport, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

class Wallet(models.Model):
    walletid = models.AutoField(primary_key=True)
    userid = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

class Expense(models.Model):
    expense_id = models.AutoField(primary_key=True)
    branch = models.ForeignKey('Branch', on_delete=models.CASCADE)
    date = models.DateField(("Date"), auto_now_add=True)
    income = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    expense = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    num_workers = models.IntegerField()
    status = models.CharField(max_length=10,null=True, blank=True )
    target = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"Expense - {self.date} - Income: {self.income}, Expense: {self.expense}, Workers: {self.num_workers}"

    def save(self, *args, **kwargs):
        self.date = self.date.replace(day=1)  # Set the day to 1 to only store the month
        super().save(*args, **kwargs)

class ExpenseHistory(models.Model):
    branch = models.ForeignKey('Branch', on_delete=models.CASCADE)
    month = models.DateField()
    income = models.DecimalField(max_digits=10, decimal_places=2)
    expense = models.DecimalField(max_digits=10, decimal_places=2)
    num_workers = models.IntegerField()

    def __str__(self):
        return f"Expense History - {self.branch} - {self.month.strftime('%B %Y')}"