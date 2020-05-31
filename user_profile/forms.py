######## Python libraries ########
from datetime import date

######## Django libraries #######
from django import forms
from .models import Profile

class ProfileModelForm(forms.ModelForm):
    class Meta:
        model = Profile
        # below are the fields that will be used in our goal form when a user creates a new goal
        fields = ['image']

    def __init__(self, *args, **kwargs):
        super(ProfileModelForm, self).__init__(*args, **kwargs)
        self.fields['image'].required           = False
