from django.shortcuts import render, get_object_or_404
from .models import Task
from .forms import TaskModelForm

def home(request):
    # Basic function based view
    my_title = "Hello there"
    context = {"title": my_title, "my_list": [1, 2, 3, 4, 5]}
    return render(request, "home.html", context)

def create_task(request):
    form = TaskModelForm(request.POST or None)
    if form.is_valid():
        print(form.cleaned_data)
        # obj = Task.objects.create(**form.cleaned_data) grabs all the fields from the forms and stores them in the Task
        obj = form.save(commit=False)
        # obj = Task.objects.create(**form.cleaned_data)
        # you can do intermediate steps with the class based models
        #obj.responsible = form.cleaned_data.get('responsible') + "0"
        obj.save()
        # Reinitialize the form
        form = TaskModelForm()
    template_name = 'task/form.html'

    # the form gets all the data that will be passed along
    context = {'form': form}
    return render(request, template_name, context)


def delete_task(request):
    template_name = 'task/delete.html'
    context = {'form': None}
    return render(request, template_name, context)

def update_task(request):
    template_name = 'task/update.html'
    context = {'form': None}
    return render(request, template_name, context)

def view_tasks(request):
    pass

def view_task_details(request):
    pass
