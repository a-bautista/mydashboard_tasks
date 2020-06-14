from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from datetime import date, datetime
from .forms import CategoryModelForm
from .models import Category

from django.contrib.auth import get_user_model
User = get_user_model()

@login_required
def create_category(request):
    '''You are passing the form CategoryModel into the template, so it can render it.'''
    form_create = CategoryModelForm(request.POST or None)
    
    username_id = None
    if request.user.get_username():    
        username_id = User.objects.get(id=request.user.id)

    if form_create.is_valid():
        category = form_create.save(commit=True) #save the goal
        category.accounts.add(username_id) # associate the category with the user
        category.save()

        # Clean the form
        form_create = CategoryModelForm()
        return redirect('/main/')
   
    template_name = 'category/formCategory.html'
    context = {'form': form_create}
    return render(request, template_name, context)


@login_required
def retrieve_all(request):
    '''Get the list of all goals during the year'''
    template_name = 'category/formRetrieval.html'
    
    #user -> category
    qs_current_user_category = Category.objects.filter(accounts=request.user.id)

    if qs_current_user_category:
        form = {'category_list': qs_current_user_category}
    else:
        form = {'category_list':[]}
    
    return render(request, template_name, form)


@login_required
def update_category(request, id):
    '''Update a category'''
    category = Category.objects.get(pk=id)  
    form = CategoryModelForm(request.POST or None, instance=category) 

    if request.method == "GET":
        template_name = 'category/formCategory.html'
        return render(request, template_name, {'form': form})

    elif request.method == "POST":
        if form.is_valid():
            form.save()
        return redirect('/main/')


# @login_required
# def delete_category(request, id):
#     '''Delete a category'''
#     category = Category.objects.get(pk=id) 
#     if request.method == "POST":
#         category.delete() 
#     return redirect('/main/')

