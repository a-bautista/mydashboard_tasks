import os
from django import forms
#from .models import User # call the model User that was created in the models of this app
from django.contrib.auth import get_user_model # this belongs from the main Django configuration and it has been customized
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import EmailConfirmed
from django.conf import settings


from datetime import datetime, timedelta
from django.core.mail import send_mail
from django.template.loader import render_to_string

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import * 


'''We will be using the customized User model from Django to store all our users which will be stored in a postgresql db.'''
User = get_user_model()

class UserRegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    
    def activate_user_email(self, context):
        activation_url = "http://localhost/activate/"+context['activation_key']
        
        message = Mail(
            from_email=settings.EMAIL,
            to_emails=context['email'],
            subject='Activate your Telos Account',
            html_content='Hello '+context['username']+',<br /><br />Please use the following link to activate your Telos account:<br /><br />'+activation_url+'<br /><br /> Thank you!<br />The Telos Team')
        try:
            sg = SendGridAPIClient(api_key=settings.API_KEY)
            response = sg.send(message)
            print(response.status_code)
            print(response.body)
            print(response.headers)
        except Exception as e:
            print(e.message)
