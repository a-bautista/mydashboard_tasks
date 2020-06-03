######## Python libraries ########
from datetime import date

######## Django libraries #######
from django import forms
from .models import Profile


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name','last_name','image']

class AppUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['task_increase_point', 'max_task_life_week']