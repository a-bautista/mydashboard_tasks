######## Python libraries ########
from datetime import date

######## Django libraries #######
from django import forms
#from django.forms.fields import DateField
#from django.contrib.admin.widgets import AdminDateWidget
from .models import Task
from django.apps import apps
#from goal.models import Goal

'''Declare the class to indicate the data that will be stored. '''
Goal = apps.get_model('goal', 'Goal') # app_name and model_name
User = apps.get_model('accounts', 'Account')
Category = apps.get_model('category', 'Category')

'''Declare the class to indicate the data that will be stored. 
    I want the goals of the logged in user who are in progress.
'''

class DropDownMenuGoalsForm(forms.Form):
    def __init__(self, *args, **kwargs):
        user_id = kwargs.pop('id')
        super(DropDownMenuGoalsForm, self).__init__(*args, **kwargs)
        self.fields['goal'] = forms.ModelChoiceField(queryset = Goal.objects.values_list('goal',flat=True).filter(accounts=User.objects.get(id=user_id),status='In Progress'), empty_label="Select your goal")


class DropDownMenuSelectedGoalsForm(forms.Form):

    def __init__(self, *args, **kwargs):
        user_id = kwargs.pop('id')
        super(DropDownMenuSelectedGoalsForm, self).__init__(*args, **kwargs)
        self.fields['goal'] = forms.ModelChoiceField(queryset = Goal.objects.values_list('goal',flat=True)
                                                    .filter(accounts=User.objects.get(id=user_id),
                                                    status='In Progress'), empty_label=None, to_field_name='goal')

class DropDownMenuCategoryForm(forms.Form):
    def __init__(self, *args, **kwargs):
        user_id = kwargs.pop('id')
        super(DropDownMenuCategoryForm, self).__init__(*args, **kwargs)
        self.fields['category'] = forms.ModelChoiceField(queryset = Category.objects.values_list('category',flat=True).filter(accounts=User.objects.get(id=user_id)), empty_label="Select your category")


class DropDownMenuSelectedCategoryForm(forms.Form):
    def __init__(self, *args, **kwargs):
        user_id = kwargs.pop('id')
        super(DropDownMenuSelectedCategoryForm, self).__init__(*args, **kwargs)
        self.fields['category'] = forms.ModelChoiceField(queryset = Category.objects.values_list('category',flat=True).filter(accounts=User.objects.get(id=user_id)), empty_label=None)


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
        choices=[(x, x) for x in range(2019, 2026)], initial=date.today().year)


class DropDownMenuMonthsForm(forms.Form):
    months = ("1",'January'),("2",'February'),("3",'March'),("4",'April'),("5",'May'),("6",'June'),\
             ("7",'July'), ("8",'August'),("9",'September'),("10",'October'),("11",'November'),("12",'December')

    month = forms.ChoiceField(choices=[x for x in months], initial=date.today().month)
    year = forms.ChoiceField(choices=[(x,x) for x in range (2019,2026)],initial=date.today().year)


class DropDownMenuYearsForm(forms.Form):
     year = forms.ChoiceField(choices=[(x, x) for x in range(2019, 2026)], initial=date.today().year)

''' 
    Instead of using the obj = Task.objects.create(**form.cleaned_data) in the view, you can
    declare a class based model that will insert all the fields into the right place of the model.  
'''

class TaskModelForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['task', 'status', 'ending_date', 'points']
        # this is necessary for the calendar
        widgets = {
            'ending_date': DateInput(),
        }


    def __init__(self, *args, **kwargs):
        super(TaskModelForm, self).__init__(*args, **kwargs)
        #self.fields['username'].required = False    # This field is mandatory, so you can insert the username_id in the task table.
        self.fields['task'].required   = True 
        self.fields['status'].required = False      # I had to make this field to false, so when you insert a record it doesn't tell you that the field is mandatory
        self.fields['points'].required = False      # I had to make this field to false, so when you insert a record it doesn't tell you that the field is mandatory
        self.fields['ending_date'].required = False # I had to make this field to false, so when you insert a record it doesn't tell you that the field is mandatory