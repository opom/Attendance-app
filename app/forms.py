from django.forms import ModelForm,DateInput
from .models import EmployeeRegistration



# Create the form class
class EmployeeForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(EmployeeForm, self).__init__(*args, **kwargs)
        # Making location required
        self.fields['name'].required = True
        self.fields['contact_no'].required = True
        self.fields['email'].required = True
        self.fields['designation'].required = True
        self.fields['department'].required = True
        self.fields['jobs'].required = True
        self.fields['date_of_joining'].required = True


    class Meta:

        model = EmployeeRegistration
        fields = ['name','contact_no','email','designation', 'department', 'jobs','date_of_joining']
        widgets = {
            'date_of_joining': DateInput(format=('%m/%d/%Y'),
                                             attrs={'class': 'form-control', 'placeholder': 'Select a date',
                                                    'type': 'date'}),
        }

