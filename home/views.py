from django.shortcuts import render
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your views here.

def index(request):
    if request.method == 'GET':
        template_name = 'home/index.html'
        username_id = None

        if request.user.id:                                         # if the user is logged in then send the user_id to the context
            username_id = User.objects.get(id=request.user.id)      # so, base_home.html can display the main site or login button
            context = {username_id:'user'}
        else:
            context = {username_id:''}                              # if no user is found, then just display the normal index page
        return render(request, template_name, context)
    
