from django import forms
#from .models import User # call the model User that was created in the models of this app
from django.contrib.auth import get_user_model # this belongs from the main Django configuration and it has been customized
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

'''We will be using the customized User model from Django to store all our users which will be stored in a postgresql db.'''
User = get_user_model()

class UserRegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

        

#class UserAuthenticateForm(AuthenticationForm):

    #class Meta:
        #model
        #pass