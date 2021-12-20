from django.contrib import admin
from .models import EmployeeRegistration,Timestamp


class EmployeeRegistrationAdmin(admin.ModelAdmin):
    list_display =[ 'name','Employeeid','email','designation','department','jobs','date_of_joining']


admin.site.register(EmployeeRegistration, EmployeeRegistrationAdmin)


class TimestampAdmin(admin.ModelAdmin):
    list_display = ['name','Employeeid','login_time','logout_time','duration','extraHours']


admin.site.register(Timestamp, TimestampAdmin)






