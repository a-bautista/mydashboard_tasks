######## Python libraries ########
from datetime import date

######## Django libraries #######
from django import forms
#from django.forms.fields import DateField
#from django.contrib.admin.widgets import AdminDateWidget
from .models import Task, User_Points

'''Declare the class to indicate the data that will be stored. '''

class TaskForm(forms.Form):
    task = forms.CharField()
    category = forms.ChoiceField(
        choices=[(x, x) for x in range(len(Task.CATEGORIES))])


class DateInput(forms.DateInput):
    input_type = 'date'


class DropDownMenuForm(forms.Form):
    # start the current week in Monday and end in Sunday
    week = forms.ChoiceField(choices=[(x, x) for x in range(
        1, 53)], initial=date.today().isocalendar()[1])
    year = forms.ChoiceField(
        choices=[(x, x) for x in range(2019, 2022)], initial=date.today().year)


class DropDownMenuMonthsForm(forms.Form):
    months = ("1",'January'),("2",'February'),("3",'March'),("4",'April'),("5",'May'),("6",'June'),\
             ("7",'July'), ("8",'August'),("9",'September'),("10",'October'),("11",'November'),("12",'December')

    month = forms.ChoiceField(choices=[x for x in months], initial=date.today().month)
    year = forms.ChoiceField(choices=[(x,x) for x in range (2019,2025)],initial=date.today().year)


class DropDownMenuYearsForm(forms.Form):
     year = forms.ChoiceField(choices=[(x, x) for x in range(2019, 2025)], initial=date.today().year)

''' 
    Instead of using the obj = Task.objects.create(**form.cleaned_data) in the view, you can
    declare a class based model that will insert all the fields into the right place of the model.  
'''

class TaskModelForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['task', 'category', 'status', 'ending_date', 'points']
        # this is necessary for the calendar
        widgets = {
            'ending_date': DateInput(),
        }


    def __init__(self, *args, **kwargs):
        super(TaskModelForm, self).__init__(*args, **kwargs)
        # I had to make this field to false, so when you insert a record it doesn't tell you that the field is mandatory
        self.fields['task'].required = True
        self.fields['status'].required = False
        self.fields['points'].required = False
        self.fields['ending_date'].required = False


class User_PointsForm(forms.ModelForm):
    class Meta:
        model = User_Points
        fields = ['id', 'points']
        

