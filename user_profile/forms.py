######## Python libraries ########
from datetime import date

######## Django libraries #######
from django import forms
from .models import Profile

class ProfileModelForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name','last_name','score','image']

    def __init__(self, *args, **kwargs):
        super(ProfileModelForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = False
        self.fields['last_name'].required  = False
        self.fields['score'].required      = True
        self.fields['image'].required      = False


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name','last_name','image']