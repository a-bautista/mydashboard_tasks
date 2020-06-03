from django.shortcuts import render, redirect, render_to_response, Http404
from django.contrib.auth import login, authenticate
from .forms import ProfileUpdateForm, AppUpdateForm
from django.contrib.auth.decorators import login_required

    
@login_required
def view_user_settings(request):

    if request.method == 'GET':
        template_name = 'user_profile/user_settings.html'
        p_form = ProfileUpdateForm(request.POST or None, instance=request.user.profile)
        return render(request, template_name, {'form': p_form})

    elif request.method == 'POST':
        p_form = ProfileUpdateForm(request.POST or None, request.FILES, instance=request.user.profile)     
        if p_form.is_valid():
            p_form.save()
    return redirect('/main/')

@login_required
def view_app_settings(request):

    if request.method == 'GET':
        template_name = 'user_profile/app_settings.html'
        s_form = AppUpdateForm(request.POST or None, instance=request.user.profile)
        return render(request, template_name, {'form': s_form})

    elif request.method == 'POST':
        s_form = AppUpdateForm(request.POST or None, request.FILES, instance=request.user.profile)     
        if s_form.is_valid():
            s_form.save()
    return redirect('/main/')