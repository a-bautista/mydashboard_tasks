from django import forms
from .models import Task

class TaskForm(forms.Form):
    responsible = forms.CharField()
    task = forms.CharField()
    initial_date = forms.DateField()
    ending_date = forms.DateField()

class TaskModelForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['responsible', 'task', 'initial_date', 'ending_date']
