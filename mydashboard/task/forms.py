######## Python libraries ########
from datetime import date

######## Django libraries #######
from django import forms
from .models import Task

'''Declare the class to indicate the data that will be stored. '''


class TaskForm(forms.Form):
    task = forms.CharField()
    category = forms.ChoiceField(
        choices=[(x, x) for x in range(len(Task.CATEGORIES))])


class DropDownMenuForm(forms.Form):
    # start the current week in Monday and end in Sunday
    week = forms.ChoiceField(choices=[(x, x) for x in range(
        1, 53)], initial=date.today().isocalendar()[1])
    year = forms.ChoiceField(
        choices=[(x, x) for x in range(2019, 2022)], initial=date.today().year)


''' 
    Instead of using the obj = Task.objects.create(**form.cleaned_data) in the view, you can
    declare a class based model that will insert all the fields into the right place of the model.  
'''


class TaskModelForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['task', 'category']

    def __init__(self, *args, **kwargs):
        super(TaskModelForm, self).__init__(*args, **kwargs)
        #self.fields['category'].empty_label = "Select"
        self.fields['task'].required = True
