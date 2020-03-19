from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import GoalModelForm
from .models import Goal

from django.contrib.auth import get_user_model
User = get_user_model()

# see your goals
#goals = Goal.objects.filter(initial_date__gte='2020-03-15', initial_date__lte='2020-03-31', accounts=2)

@login_required
def create_goal(request):
    '''You are passing the form GoalModel into the template, so it can render it.'''
    form_create = GoalModelForm(request.POST or None)
    #goals_dropdownmenu = DropDownMenuGoalsForm()
    
    username_id = None
    if request.user.get_username():    
        username_id = User.objects.get(id=request.user.id)

    
    if form_create.is_valid():
        goal = form_create.save(commit=True) #save the goal
        goal.accounts.add(username_id) # relate the goal  users table and the goal_user_table
        goal.save() 
        # Clean the form
        form_create = GoalModelForm()
        return redirect('/tasks/')
    #else:
        #print(form_create)
        
    template_name = 'goal/formGoal.html'
    # the form keyword gets all the data that will be passed along to the formCreate template
    context = {'form': form_create
    
     }
    return render(request, template_name, context)