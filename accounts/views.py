from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from .forms import UserRegisterForm, AuthenticationForm
from django.contrib.auth.decorators import login_required

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST) # this UserRegisterForm is based on the UserCreationForm which has custom fields
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account {username} has been successfully created!')
            #login(request, username)
            return redirect('login')
            #return redirect('/')
    else:    
        form = UserRegisterForm()
        #messages.error(request, f'{messages}: {form.error_messages}')
    return render(request, 'accounts/register.html', {'form': form})


#def login(request):
#    form = AuthenticationForm(request.POST)
#    return render(request, 'accounts/login.html', {"form": form})

@login_required
def profile(request):
    return render(request, 'accounts/profile.html')