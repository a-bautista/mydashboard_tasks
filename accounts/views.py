from django.shortcuts import render, redirect, render_to_response
from django.contrib.auth import login, authenticate
from django.contrib import messages
from .forms import UserRegisterForm, AuthenticationForm
from django.contrib.auth.decorators import login_required


def register(request):
    form = UserRegisterForm(request.POST) # this UserRegisterForm is based on the UserCreationForm which has custom fields
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account {username} has been successfully created!')
            return redirect('login')
        else:
            # display the errors when trying to submit your request
            #return render_to_response('accounts/register.html', {'form':form})
            return render(request, 'accounts/register.html', {'form':form})
    elif request.method == 'GET':    
        form = UserRegisterForm()
    return render(request, 'accounts/register.html', {'form': form})
    

#def login(request):
#    form = AuthenticationForm(request.POST)
#    return render(request, 'accounts/login.html', {"form": form})

@login_required
def profile(request):
    return render(request, 'accounts/profile.html')

# messages.debug
# messages.info
# messages.success
# messages.warning
# messages.error


 
#<django.contrib.messages.storage.fallback.FallbackStorage object at 0x7f1da8ac3978>
#Your account a5 has been successfully created!