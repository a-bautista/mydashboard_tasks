######## Python libraries ########
from datetime import date

######## Django libraries #######
from django import forms
from .models import Goal

class DateInput(forms.DateInput):
    input_type = 'date'

class GoalModelForm(forms.ModelForm):
    class Meta:
        model = Goal
        # below are the fields that will be used in our goal form when a user creates a new goal
        fields = ['goal', 'initial_date', 'expiration_date', 'status', 'comments', 'final_notes']
        # this is necessary for the calendar
        widgets = {
            'initial_date': DateInput(),
            'expiration_date': DateInput()
        }


    def __init__(self, *args, **kwargs):
        super(GoalModelForm, self).__init__(*args, **kwargs)
        self.fields['goal'].required            = True 
        self.fields['initial_date'].required    = True
        self.fields['expiration_date'].required = True
        self.fields['status'].required          = False  # I had to make this field to false, so when you insert a record it doesn't tell you that the field is mandatory
        self.fields['comments'].required        = False # I had to make this field to false, so when you insert a record it doesn't tell you that the field is mandatory
        self.fields['final_notes'].required     = False # I had to make this field to false, so when you insert a record it doesn't tell you that the field is mandatory

    #def __str__(self):
    #    return self.goal