from django.forms import ModelForm,DateInput
from .models import EmployeeRegistration



# Create the form class
class EmployeeForm(ModelForm):
   class Meta:
        model = EmployeeRegistration
        fields = ['name','contact_no','email','designation', 'department', 'jobs','date_of_joining']
        widgets = {
            'date_of_joining': DateInput(format=('%m/%d/%Y'),
                                             attrs={'class': 'form-control', 'placeholder': 'Select a date',
                                                    'type': 'date'}),
        }

