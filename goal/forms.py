######## Python libraries ########
from datetime import date

######## Django libraries #######
from django import forms
#from django.forms.fields import DateField
#from django.contrib.admin.widgets import AdminDateWidget
from .models import Goal

'''Declare the class to indicate the data that will be stored. '''


class DateInput(forms.DateInput):
    input_type = 'date'
    

class GoalModelForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = ['goal', 'expiration_date']
        # this is necessary for the calendar
        widgets = {
            'expiration_date': DateInput(),
        }


    '''def __init__(self, *args, **kwargs):
        super(TaskModelForm, self).__init__(*args, **kwargs)
        self.fields['username'].required = False    # This field is mandatory, so you can insert the username_id in the task table.
        self.fields['task'].required   = True 
        self.fields['status'].required = False      # I had to make this field to false, so when you insert a record it doesn't tell you that the field is mandatory
        self.fields['points'].required = False      # I had to make this field to false, so when you insert a record it doesn't tell you that the field is mandatory
        self.fields['ending_date'].required = False # I had to make this field to false, so when you insert a record it doesn't tell you that the field is mandatory
    '''
        

