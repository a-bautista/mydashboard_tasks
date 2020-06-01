from django.shortcuts import render, redirect, render_to_response, Http404
from django.contrib.auth import login, authenticate
from .forms import ProfileModelForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required

# from django.contrib.auth import get_user_model
# User = get_user_model()
    
@login_required
def view_user_settings(request):

    if request.method == 'POST':
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if p_form.is_valid():
            p_form.save()
            return redirect('/main/')

    else:
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'p_form':p_form,
    }

    return render(request, 'user_profile/user_settings.html', context)