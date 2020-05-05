from django import forms
#from .models import User # call the model User that was created in the models of this app
from django.contrib.auth import get_user_model # this belongs from the main Django configuration and it has been customized
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import EmailConfirmed

from django.core.mail import send_mail
from django.template.loader import render_to_string

'''We will be using the customized User model from Django to store all our users which will be stored in a postgresql db.'''
User = get_user_model()

class UserRegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class LoginForm(forms.Form):
    #email    = forms.CharField()
    #username = forms.CharField()
    #password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['username', 'password1']

    # def clean_email(self):
    #     username = self.cleaned_data.get("username")
    #     try:
    #         user = User.objects.get(username=username)
    #     except User.DoesNotExist:
    #         raise forms.ValidationError("Are you sure you are registered? We cannot find this user.")
    #     return username

    # def clean_password(self):
    #     username = self.cleaned_data.get("username")
    #     password = self.cleaned_data.get("password")

    #     try:
    #         user = User.objects.get(username=username)
    #     except:
    #         user = None
    #     if user is not None and not user.check_password(password):
    #         raise forms.ValidationError("Invalid Password")
    #     elif user is None:
    #         pass
    #     else:
    #         return password

class EmailConfirmedForm(forms.ModelForm):
    
    class Meta:
        model = EmailConfirmed
        fields = ['username', 'activation_key', 'confirmed']
      

    def activate_user_email(self):
        #send email here and render string
        activation_url = "http://localhost/accounts/activate/%s" %(self.activation_key)
        context = {
               "activation_key": self.activation_key,
               "activation_url": activation_url
        }
        subject = "Activate your Email"
        message = render_to_string("Accounts/activation_message.txt", context)
        self.email_user(subject, message, settings.DEFAULT_FROM_EMAIL)


    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email_user], **kwargs)
