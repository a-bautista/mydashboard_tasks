######## Python libraries ########
from datetime import date

######## Django libraries #######
from django import forms
from .models import Goal

class DateInput(forms.DateInput):
    input_type = 'date'

class DropDownMenuForm(forms.Form):
    # start the current week in Monday and end in Sunday
    week = forms.ChoiceField(choices=[(x, x) for x in range(
        1, 53)], initial=date.today().isocalendar()[1])
    year = forms.ChoiceField(
        choices=[(x, x) for x in range(2019, 2026)], initial=date.today().year)

class DropDownMenuQuarterlyForm(forms.Form):

    quarters = ("1",'Q1'),("2",'Q2'),("3",'Q3'),("4",'Q4')
    
    if date(date.today().year, 1, 1) <= date.today() <= date(date.today().year, 3, 31):
        initial_value = ("1",'Q1')
    elif date(date.today().year, 4, 1) <= date.today() <= date(date.today().year, 6, 30):
        initial_value = ("2",'Q2')
    elif date(date.today().year, 7, 1) <= date.today() <= date(date.today().year, 9, 30):
        initial_value = ("3",'Q3')
    elif date(date.today().year, 10, 1) <= date.today() <= date(date.today().year, 12, 31):
        initial_value = ("4",'Q4')    

    quarter = forms.ChoiceField(choices=[x for x in quarters], initial=initial_value)
    year    = forms.ChoiceField(choices=[(x, x) for x in range(2019, 2026)], initial=date.today().year)

class GoalModelForm(forms.ModelForm):
    class Meta:
        model = Goal
        # below are the fields that will be used in our goal form when a user creates a new goal
        fields = ['goal', 'initial_date', 'expiration_date', 'status', 'goal_type', 'comments', 'final_notes']
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
        self.fields['goal_type'].required       = False # I had to make this field to false, so when you insert a record it doesn't tell you that the field is mandatory
        self.fields['comments'].required        = False # I had to make this field to false, so when you insert a record it doesn't tell you that the field is mandatory
        self.fields['final_notes'].required     = False # I had to make this field to false, so when you insert a record it doesn't tell you that the field is mandatory

    #def __str__(self):
    #    return self.goal