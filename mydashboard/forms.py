from django import forms

class ContactForm(forms.Form):
    full_name = forms.CharField()
    email = forms.EmailField()
    content = forms.CharField(widget=forms.Textarea)

    '''This is used to create your own custom validators'''
    def clean_email(self, *args, **kwargs):
        email = self.cleaned_data.get('email')
        if email.endswith(".edu"):
            raise forms.ValidationError("This is not a valid email. Please don't use the .edu")
        return email