from django.shortcuts import render, redirect, render_to_response, Http404
from django.contrib.auth import login, authenticate
from .forms import ProfileModelForm
from django.contrib.auth.decorators import login_required

# from django.contrib.auth import get_user_model
# User = get_user_model()
    
@login_required
def view_user_settings(request):
    return render(request, 'user_profile/user_settings.html')

