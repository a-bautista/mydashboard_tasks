from django import forms
#from .models import User # call the model User that was created in the models of this app
from django.contrib.auth import get_user_model # this belongs from the main Django configuration and it has been customized
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import EmailConfirmed


from datetime import datetime, timedelta
from django.core.mail import send_mail
from django.template.loader import render_to_string

'''We will be using the customized User model from Django to store all our users which will be stored in a postgresql db.'''
User = get_user_model()

class UserRegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    
    def activate_user_email(self, context):
        #activation_url = "http://telos-app.xyz/activate/"+context['activation_key']
        activation_url = "http://localhost/activate/"+context['activation_key']
        email_content = {
        			      'activation_url':activation_url,
        			      'username':context['username']
        		  		}

        subject = "Activate your Telos Account"
        message = render_to_string("accounts/activation_message.txt", email_content)
        from_email = None
        send_mail(subject, message, from_email, [context['email']], fail_silently=False)

    