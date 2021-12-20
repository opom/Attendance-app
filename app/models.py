from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

import datetime


designation_choices = (
    ('Intern', 'Intern'),
    ('Full_time', 'Full Time')
)

department_choices = (
    ('Software', 'Development & IT'),
    ('Ed-tech', 'Ed-Tech'),
    ('Marketing', 'Marketing'),
    ('Design', 'Designing'),
    ('Content_writing', 'Content-Writing')
)
job_choices = (
    ('Regular', 'Regular'),
    ('Work From Home', 'Work From Home')
)

# Signup Page for Employee
class EmployeeRegistration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    Employeeid = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,12}$')
    contact_no = models.CharField(validators=[phone_regex], max_length=12, blank=True)
    email= models.EmailField()
    designation = models.CharField(max_length=20, choices=designation_choices, blank=True)
    department = models.CharField(max_length=20, choices=department_choices, blank=True)
    jobs = models.CharField(max_length=15, choices=job_choices, blank=True)
    date_of_joining = models.DateField()
    USERNAME_FIELD = 'Employeeid'

# Employee LOGIN TIME and LOGOUT TIME
def log_out_time():
    now = datetime.datetime.now()
    return now


class Timestamp(models.Model):
    id =  models.AutoField(primary_key=True)
    Employeeid = models.ForeignKey(EmployeeRegistration, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    login_time = models.DateTimeField(auto_now_add=True, blank=True)
    logout_time = models.DateTimeField(null=True,blank=True)

    @property
    def duration(self):
        if self.logout_time is not None:
            return str(self.logout_time - self.login_time)
    @property
    def extraHours(self):
        if self.logout_time is not None:
            if(int(self.duration.split(":")[0]) >= 4):
                return 1
            else:
                return 0







