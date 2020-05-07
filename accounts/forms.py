import os
from django import forms
#from .models import User # call the model User that was created in the models of this app
from django.contrib.auth import get_user_model # this belongs from the main Django configuration and it has been customized
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import EmailConfirmed


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
        #activation_url = "http://telos-app.xyz/activate/"+context['activation_key']
        activation_url = "http://localhost/activate/"+context['activation_key']
        email_content = {
        			      'activation_url':activation_url,
        			      'username':context['username']
        		  		}
       
        message = Mail(
            from_email='',
            to_emails=context['email'],
            subject='Activate your Telos Account',
            html_content=activation_url)
        try:
            sg = SendGridAPIClient(api_key='')
            response = sg.send(message)
            print(response.status_code)
            print(response.body)
            print(response.headers)
        except Exception as e:
            print(e.message)

    