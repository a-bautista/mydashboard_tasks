from django.shortcuts import render, get_object_or_404
from .models import Task

def home(request):
    # Basic function based view
    my_title = "Hello there"
    context = {"title": my_title, "my_list": [1, 2, 3, 4, 5]}
    return render(request, "home.html", context)

def create_task(request):
    
    template_name = 'create_task.html'
    context = {'form': None}
    return render(request, template_name, context)


def delete_task(request):
    pass

def update_task(request):
    pass

def view_tasks(request):
    pass

def view_task_details(request):
    pass
