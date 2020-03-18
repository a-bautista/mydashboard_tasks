from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import CategoryModelForm
from .models import Category

# Create your views here.
@login_required
def create_category(request):
    form_create = CategoryModelForm(request.POST or None)

    if form_create.is_valid():
        category = form_create.save(commit=True) #save the goal
        category.save() 
        # Clean the form
        form_create = CategoryModelForm()
        return redirect('/tasks/')

    template_name = 'category/formCategory.html'
    # the form keyword gets all the data that will be passed along to the formCreate template
    context = {'form': form_create}
    return render(request, template_name, context)