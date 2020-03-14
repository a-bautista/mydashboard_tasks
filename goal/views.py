from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import GoalModelForm, DropDownMenuGoalsForm
from .models import Goal

@login_required
def create_goal(request):
    '''You are passing the form GoalModel into the template, so it can render it.'''
    form_create = GoalModelForm(request.POST or None)
    goals_dropdownmenu = DropDownMenuGoalsForm()
    
    #username_id = None
    #if request.user.get_username():    
    #    username_id = User.objects.get(id=request.user.id)
    
    if form_create.is_valid():
        obj = form_create.save(commit=False)
        # obj.username = username_id # save the username_id in the task_task table
        obj.save() 
        # Clean the form
        form_create = GoalModelForm()
        return redirect('/tasks/')
    #else:
        #print(form_create)
        
    template_name = 'goal/formGoal.html'
    # the form keyword gets all the data that will be passed along to the formCreate template
    context = {'form': form_create, 'goals_dropdownmenu': goals_dropdownmenu}
    return render(request, template_name, context)