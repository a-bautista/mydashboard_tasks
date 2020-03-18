######## Python libraries ########
from datetime import date

######## Django libraries #######
from django import forms
from .models import Category

class CategoryModelForm(forms.ModelForm):
    class Meta:
        model = Category
        # below are the fields that will be used in our goal form when a user creates a new goal
        fields = ['category', 'comments']


    def __init__(self, *args, **kwargs):
        super(CategoryModelForm, self).__init__(*args, **kwargs)
        self.fields['category'].required    = True 
        self.fields['comments'].required    = True
