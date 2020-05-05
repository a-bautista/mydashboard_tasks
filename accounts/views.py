from django.shortcuts import render, redirect, render_to_response
from django.contrib.auth import login, authenticate
from django.contrib import messages
from .forms import UserRegisterForm, EmailConfirmedForm, LoginForm
from django.contrib.auth.decorators import login_required

def register_view(request):
    form = UserRegisterForm(request.POST) # this UserRegisterForm is based on the UserCreationForm which has custom fields
    #email_registration = EmailConfirmedForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account {username} has been successfully created!')
            #print(EmailConfirmed.activate_user_email(EmailConfirmed))
            #print(email_registration.)
            #print(email_registration.activate_user_email())
            
            return redirect('login')
        else:
            # display the errors when trying to submit your request
            #return render_to_response('accounts/register.html', {'form':form})
            return render(request, 'accounts/register.html', {'form':form})
    elif request.method == 'GET':    
        form = UserRegisterForm()
    return render(request, 'accounts/register.html', {'form': form})
    

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
