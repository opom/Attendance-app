from django.db import models
from django.contrib.auth.models import User

import datetime


designation_choices = (
    ('intern', 'Intern'),
    ('full_time', 'Full Time')
)

department_choices = (
    ('software', 'Development & IT'),
    ('ed_tech', 'Ed-Tech'),
    ('marketing', 'Marketing'),
    ('design', 'Designing'),
    ('content_writing', 'Content-Writing')
)
job_choices = (
    ('on_site', 'Regular'),
    ('WFH', 'Work From Home')
)

# Signup Page for Employee
class EmployeeRegistration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    Employeeid = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    contact_no = models.IntegerField(max_length=10)
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
        return str(self.logout_time - self.login_time)
    @property
    def extraHours(self):
        if(int(self.duration.split(":")[0]) >= 4):
            return 1
        else:
            return 0







