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

    
    # def activate_user_email(self, context):
    #     activation_url = "http://www.telos-app.xyz/activate/"+context['activation_key']
        
    #     message = Mail(
    #         from_email=os.environ['EMAIL_HOST_USER'],
    #         to_emails=context['email'],
    #         subject='Activate your Telos Account',
    #         html_content='Hello '+context['username']+',<br /><br />Please use the following link to activate your Telos account:<br /><br />'+activation_url+'<br /><br /> Thank you!<br />The Telos Team')
    #     try:
    #         sg = SendGridAPIClient(api_key=os.environ['SENDGRID_API_KEY'])
    #         response = sg.send(message)
    #         print(response.status_code)
    #         print(response.body)
    #         print(response.headers)
    #     except Exception as e:
    #         print(e.message)


    def activate_user_email(self, context):
        activation_url = "http://www.telos-app.xyz/activate/"+context['activation_key']
        email_content = {
        			      'activation_url':activation_url,
        			      'username':context['username']
        		  		}

        subject = "Activate your Telos account"
        message = render_to_string("accounts/activation_message.txt", email_content)
        from_email = None
        send_mail(subject, message, from_email, [context['email']], fail_silently=False)
