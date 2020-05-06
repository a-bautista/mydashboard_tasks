from django.shortcuts import render, redirect, render_to_response
from django.contrib.auth import login, authenticate
from django.contrib import messages
from .forms import UserRegisterForm
from django.contrib.auth.decorators import login_required
import hashlib, os
from datetime import datetime, timedelta

from .models import EmailConfirmed

from django.contrib.auth import get_user_model
User = get_user_model()

def register_view(request):
    form = UserRegisterForm(request.POST) # this UserRegisterForm is based on the UserCreationForm which has custom fields
    #email_registration = EmailConfirmedForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            context = {}
            context['email']    = form.cleaned_data.get('email')
            context['username'] = form.cleaned_data.get('username')
            
            # decent
            #hashlib.sha256(str(random.getrandbits(256)).encode('utf-8')).hexdigest()
            
            # generate the hash for the activation url
            short_hash = hashlib.sha256(str(os.urandom(256)).encode('utf-8')).hexdigest()[:10]
            activation_key = hashlib.sha256(str(short_hash+context['username']).encode('utf-8')).hexdigest()
            context['activation_key'] = activation_key

            # send the email with the activation hash
            UserRegisterForm.activate_user_email(UserRegisterForm,context) 

            # save the data of the activation key in the db
            #UserRegisterForm.profile_activation(UserRegisterForm, context)
            form.save()

            # Deactivate account
            username = context['username']
            user = User.objects.get(username=username)
            user.is_active = False 
            user.save()

            # save the records in the EmailConfirmed db
            profile_activation = EmailConfirmed()
            profile_activation.username = user
            profile_activation.activation_key = context['activation_key']

            # set the time expiration for the key string value
            profile_activation.key_expires = datetime.strftime(datetime.now() + timedelta(days=2), "%Y-%m-%d %H:%M:%S")
            profile_activation.save()

            messages.success(request, f'Your account {username} has been successfully created! Check your email for activating your account.')   
            return redirect('login')
        else:
            # display the errors when trying to submit your request
            #return render_to_response('accounts/register.html', {'form':form})
            return render(request, 'accounts/register.html', {'form':form})
    elif request.method == 'GET':    
        form = UserRegisterForm()
    return render(request, 'accounts/register.html', {'form': form})
    
# def login_view(request):
#     form = LoginForm(request.POST)
#     print(form)
#     if request.method == 'POST':
#         form = AuthenticationForm(data=request.POST)
#         if form.is_valid():
#             return redirect('main_dashboard')
#     else:
#         form = AuthenticationForm()
#     return render(request, 'accounts/login.html')


# def login_view(request):
#     form = LoginForm(request.POST or None)
#     if request.method == 'POST':
#         if form.is_valid():
#             username = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password')
#             user = authenticate(username=username, password=password)
            
#             if user is not None:
#                 login(request, user)
#                 return redirect('main_dashboard')
#             else:
#                 messages.info(request, 'Invalid credentials')
#                 return redirect('login')
        
#     elif request.method == 'GET':    
#         return render(request, 'accounts/login.html')
        
    
@login_required
def profile(request):
    return render(request, 'accounts/profile.html')

# messages.debug
# messages.info
# messages.success
# messages.warning
# messages.error 
#<django.contrib.messages.storage.fallback.FallbackStorage object at 0x7f1da8ac3978>
