from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import GoalModelForm
from .models import Goal
from datetime import date, datetime
from .forms import DropDownMenuForm, DropDownMenuQuarterlyForm

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
        return redirect('/main/')
    
        
    template_name = 'goal/formGoal.html'
    # the form keyword gets all the data that will be passed along to the formCreate template
    context = {'form': form_create}
    return render(request, template_name, context)


@login_required
def retrieve_all(request):
    '''Get the list of all goals during the year'''
    template_name = 'goal/formRetrieval.html'
    status_goal = 'In Progress'
    
    # year = date.today().year
    # initial_date, ending_date = get_start_end_date_yearly(year)

    goal_ids = []
    #user -> goal
    qs_current_user_goals = Goal.objects.filter(accounts=request.user.id, 
                                                            status=status_goal).values('id').values_list('id')

    for value in qs_current_user_goals:
        goal_ids.append(value[0])
    
    # current goals
    form = {'goal_list': Goal.objects.filter(id__in=goal_ids)}
    
    return render(request, template_name, form)


@login_required
def update_goal(request, id):
    '''Update a goal'''
    goal = Goal.objects.get(pk=id)  # get the task id from the db
    form = GoalModelForm(request.POST or None, instance=goal) # overwrite the task, do not create a new one

    if request.method == "GET":
        template_name = 'goal/formGoal.html'
        return render(request, template_name, {'form': form})

    # when the forms gets updated, the task disappears from the db
    elif request.method == "POST":
        if form.is_valid():
            form.save()
        return redirect('/main/')


@login_required
def delete_goal(request, id):
    '''Delete a task'''
    goal = Goal.objects.get(pk=id) # get the current points of the task
    if request.method == "POST":
        goal.delete() # delete the task from the db
    return redirect('/main/')


@login_required
def view_previous_goals_quarterly(request):
    if request.method == "GET":
        template_name = 'goal/no_retrieval_results/previous_goals_quarterly.html'
        form = DropDownMenuQuarterlyForm()
        return render(request, template_name, {'form': form})

    elif request.method == "POST":
        template_name = 'goal/retrieval_results/previous_goals_quarterly.html'
        year = request.POST.get('select_year', None)
        quarter = request.POST.get('select_quarter', None)

        initial_date = ''
        ending_date = ''

        if quarter == '1':
            initial_date = date(int(year), 1, 1) 
            ending_date  = date(int(year), 3, 31)
        elif quarter == '2':
            initial_date = date(int(year), 4, 1) 
            ending_date  = date(int(year), 6, 30)
        elif quarter == '3':
            initial_date = date(int(year), 7, 1) 
            ending_date  = date(int(year), 9, 30)
        elif quarter == '4':
            initial_date = date(int(year), 10, 1) 
            ending_date  = date(int(year), 12, 31)
        
        goal_ids = []
        #user -> goal
        qs_current_user_goals = Goal.objects.filter(initial_date__gte=initial_date, expiration_date__lte=ending_date, 
                            accounts=request.user.id).values('id').values_list('id')

        for value in qs_current_user_goals:
            goal_ids.append(value[0])
    
        for value in qs_current_user_goals:
            goal_ids.append(value[0])
    
        # current goals
        form = {'goal_list': Goal.objects.filter(id__in=goal_ids), 'year':year}
    
        return render(request, template_name, form)


@login_required
def view_previous_goals_yearly(request):
    if request.method == "GET":
        template_name = 'goal/no_retrieval_results/previous_goals_yearly.html'
        form = DropDownMenuForm()
        return render(request, template_name, {'form': form})

    elif request.method == "POST":
        template_name = 'goal/retrieval_results/previous_goals_yearly.html'
        year = request.POST.get('select_year', None)

         # Return only the initial date with 0 because the ending date can be obtained by adding 7 additional days
        initial_date, ending_date = get_start_end_date_yearly(year)
        
        goal_ids = []
        #user -> goal
        # display the goals of the current year based in their initial dates
        qs_current_user_goals = Goal.objects.filter(initial_date__gte=initial_date, 
                accounts=request.user.id).values('id').values_list('id')


        for value in qs_current_user_goals:
            goal_ids.append(value[0])
    
        for value in qs_current_user_goals:
            goal_ids.append(value[0])
    
        # current goals
        form = {'goal_list': Goal.objects.filter(id__in=goal_ids), 'year':year}
    
        return render(request, template_name, form)


def get_start_end_date_yearly(year):
    
    initial_year  = str(year)
    initial_month = str("01") #first month of the year
    initial_day   = str("01")  # first day of month as a zero padded decimal number

    ending_year   = str(year)
    ending_month  = str("12") #last month of the year
    ending_day    = str("31")  # get the last day of the month

    # Default time values
    beginning_hour   = 00
    beginning_minute = 00
    beginning_second = 00

    # Default time values
    ending_hour   = 23
    ending_minute = 59
    ending_second = 59


    initial_date  = datetime(int(initial_year), int(initial_month), int(initial_day),
                                              beginning_hour, beginning_minute, beginning_second)

    ending_date   = datetime(int(ending_year), int(ending_month), int(ending_day),
                                                ending_hour, ending_minute, ending_second)

    return initial_date, ending_date