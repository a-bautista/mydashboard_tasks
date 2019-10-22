from django import forms
from .models import Task

'''Declare the class to indicate the data that will be stored. '''
class TaskForm(forms.Form):
    responsible = forms.CharField()
    task = forms.CharField()
    initial_date = forms.DateField()

''' 
    Instead of using the obj = Task.objects.create(**form.cleaned_data) in the view, you can
    declare a class based model that will insert all the fields into the right place of the model.  
'''
class TaskModelForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['responsible', 'task', 'initial_date']

    