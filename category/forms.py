######## Django libraries #######
from django import forms

###### Models #########
from .models import Category

class CategoryModelForm(forms.ModelForm):
    class Meta:
        model = Category
        # below are the fields that will be used in our goal form when a user creates a new goal
        fields = ['category', 'description']

    def __init__(self, *args, **kwargs):
        super(CategoryModelForm, self).__init__(*args, **kwargs)
        self.fields['category'].required        = True 
        self.fields['description'].required     = False