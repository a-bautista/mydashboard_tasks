from datetime import date, datetime, timedelta, time
from django.views.generic import View
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count, TextField
from django.db.models.functions import Cast
from django.contrib.auth.decorators import login_required
from .forms import TaskModelForm, DropDownMenuForm, DropDownMenuMonthsForm, DropDownMenuYearsForm, DropDownMenuGoalsForm
#DropDownMenuCategoriesForm
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Task, Goal
import json, calendar

from django.contrib.auth import get_user_model
User = get_user_model()


@login_required
def main_dashboard(request):
    username = None
    if request.user.get_username():
        username = request.user.username
    
    user= User.objects.filter(username=username).values('score').values_list('score')[0][0]
    week = date.today().isocalendar()[1]
    month = datetime.today().month
    year  = datetime.today().year
    quarter   = (month-1)//3+1
    
    initialDayQuarter = datetime(year, 3 * quarter - 2, 1)
    lastDayQuarter    = datetime(year, (3 * quarter)%12+1, 1) + timedelta(days=-1)

    context = { "points": user, "month": datetime.now().strftime("%B"), "week": week, 
                "initial_date_quarter": initialDayQuarter, "lastDayQuarter":lastDayQuarter } # display the current points, current month, current week
    return render(request, 'task/mainDashboard.html', context)


class Dashboard_Categories_Month(APIView):

    def get(self, request, *args, **kwargs):
        year = date.today().year
        month = date.today().month
        initial_date, ending_date = get_start_end_date_monthly(year, month)

        goal_ids = []   
        qs_current_user_goals = Goal.objects.filter(initial_date__gte=initial_date, initial_date__lte=ending_date, 
                            accounts=request.user.id).values('id').values_list('id')

        for value in qs_current_user_goals:
            goal_ids.append(value)


        qs_group_by = Task.objects.values(
            'category').annotate(count=Count('category')).filter(goal__in = goal_ids).order_by('count')

        keys_graph = list(qs_group_by.values_list('category'))
        values_graph = list(qs_group_by.values_list('count'))
        front_end_dictionary = {
            "labels_graph": keys_graph,
            "values_graph": values_graph
        }
        return Response(front_end_dictionary)


class Dashboard_Status_Month(APIView):

    def get(self, request, *args, **kwargs):
        year = date.today().year
        month = date.today().month
        initial_date, ending_date = get_start_end_date_monthly(year, month)

        goal_ids = []   
        qs_current_user_goals = Goal.objects.filter(initial_date__gte=initial_date, initial_date__lte=ending_date, 
                            accounts=request.user.id).values('id').values_list('id')

        for value in qs_current_user_goals:
            goal_ids.append(value)


        # there's an error when you start having different tasks, they are not counting, really?
        qs_group_by = Task.objects.values(
            'status').annotate(count=Count('status')).filter(goal__in = goal_ids).order_by('count')


        keys_graph = list(qs_group_by.values_list('status'))
        values_graph = list(qs_group_by.values_list('count'))
        front_end_dictionary = {
            "labels_graph": keys_graph,
            "values_graph": values_graph
        }
        return Response(front_end_dictionary)


class Dashboard_Tasks_Week(APIView):

    def get(self, request, *args, **kwargs):

        '''Show only the results of the logged in user'''
        year = date.today().year
        week = date.today().isocalendar()[1]
        standard_increase_points = 1.25
        last_increase_points = 1.50

        # Return only the initial date with 0 because the ending date can be obtained by adding 7 additional days
        #initial_date, ending_date = get_start_end_date(year, week)

        goal_ids = []   
        # goals -> users
        qs_current_user_goals = Goal.objects.filter(accounts=request.user.id).values('id').values_list('id')

        for value in qs_current_user_goals:
            goal_ids.append(value)

        # tasks -> goals
        qs = Task.objects.filter(goal__in=goal_ids, status='Active')
        # qs = Task.objects.filter(status='Active').values() # when you add values, you convert the queryset into a dictionary

        '''The following is the system that increases the points of tasks based on the amount of time they have been in your stack of tasks.
            
            Each task has 4 lives and for every week that has passed, a task loses points. 
            The amount of time a task has been in the queue is based on the current date - the initial date a task was first created.
            1 to 7 days   - A task has 4 lives and no increase of points are done.
            8 to 14 days  - A task has 3 lives and there's an increase of points of 25%.
            15 to 21 days - A task has 2 lives and there's an increase of points of 25%.
            22 to 28 days - A task has 1 life and there's an increase of points of 50%.
            Over 28 days, tasks are cancelled and you lose the points that were accrued on those tasks. 
            '''
        for task in qs:
            if (datetime.now()-datetime.combine(task.initial_date,time())) >= timedelta(days=7) and (datetime.now()-datetime.combine(task.initial_date,time())) < timedelta(days=14) and task.life_task == 3:
                task.points = task.points*standard_increase_points
                task.life_task = task.life_task - 1
            elif (datetime.now()-datetime.combine(task.initial_date,time())) >= timedelta(days=14) and (datetime.now()-datetime.combine(task.initial_date,time())) < timedelta(days=21) and task.life_task == 2:
                task.points = task.points*standard_increase_points
                task.life_task = task.life_task - 1
            elif (datetime.now()-datetime.combine(task.initial_date,time())) >= timedelta(days=21) and (datetime.now()-datetime.combine(task.initial_date,time())) < timedelta(days=28) and task.life_task == 1:
                task.points = task.points*last_increase_points
                task.life_task = task.life_task - 1
            elif (datetime.now()-datetime.combine(task.initial_date,time())) >= timedelta(days=28) and task.life_task == 0:
                
                # cancel the task
                task.status='Cancelled'
                # insert the task date when the task gets cancelled
                task.ending_date = datetime.now()
                # decrease the points from the general counter
                
                #user_points = User_Points.objects.filter(id=1) # get our only user from the db
                #holder = int(list(User_Points.objects.filter(id=1).values('points').values_list('points'))[0][0])
                #holder = int(list(User.objects.filter(username_id=Cast(request.user.id, TextField())).values('score').values_list('score'))[0][0])
                holder = User.objects.filter(id=request.user.id).values('score').values_list('score')[0][0] # get the points of the form with section points
                User.objects.filter(id=request.user.id).update(score=holder-int(task.points)) # subtract the points from the general score
            task.save()
  
        x_axis = list(qs.values_list('task'))
        y_axis = list(qs.values_list('points'))

        front_end_dictionary = {
            "labels_graph": x_axis,
            "values_graph": y_axis
        }
        return Response(front_end_dictionary)


class Dashboard_Goals_Quarter(APIView):
    ''' Display all the goals and indicate the % of progress in each one once they have been finalized. '''
    def get(self, request, *args, **kwargs):

        '''Show only the results of the logged in user'''
        year  = date.today().year
        month = date.today().month
        quarter   = (month-1)//3+1
        initialDayQuarter = datetime(year, 3 * quarter - 2, 1)
        lastDayQuarter    = datetime(year, (3 * quarter)%12+1, 1) + timedelta(days=-1)

        # Return only the initial date with 0 because the ending date can be obtained by adding 7 additional days
        #initial_date, ending_date = get_start_end_date(year, week)

        goal_task_finalized = {}
        #goal_task_cancelled = {}
        #goal_task_active    = {}
        goal_task_total     = {}

        finalized_task_goal_count = {}
        total_task_goal_count     = {}
        percentages_task_goals    = {}


        goal_ids = []   
        # goals -> users
        qs_current_user_goals_quarter = Goal.objects.filter(accounts=request.user.id, 
                                                            initial_date__gte=initialDayQuarter, 
                                                            initial_date__lte=lastDayQuarter).values('id','goal').values_list('id','goal')

        for id, value in enumerate(qs_current_user_goals_quarter):
            goal_task_finalized[value[1]] = Task.objects.values('goal').order_by().annotate(task_goal_count=Count('goal')).filter(goal=value[0], status='Finalized')
            goal_task_total[value[1]] = Task.objects.values('goal').order_by().annotate(task_goal_count=Count('goal')).filter(goal=value[0])

        finalized_goals, qs_finalized = zip(*goal_task_finalized.items())
        total_goals,     qs_total     = zip(*goal_task_total.items())

        
        for goal in finalized_goals:
            for element in goal_task_finalized[goal]:
                finalized_task_goal_count[goal] = element['task_goal_count']

        for goal in total_goals:
            for element in goal_task_total[goal]:
                total_task_goal_count[goal] = element['task_goal_count']

        print(total_task_goal_count,finalized_task_goal_count)
        
        for goal in total_goals:
            try:
                percentages_task_goals[goal] = (finalized_task_goal_count[goal]*100)/total_task_goal_count[goal]
            except:
                # assign the goal that doesn't have any finalized task to 0, so you can visualize it in the graph
                percentages_task_goals[goal] = 0

        print(percentages_task_goals)
        x_axis, y_axis = zip(*percentages_task_goals.items())

        #qs_current_user_goals_quarter = Goal.objects.filter(accounts=1, 
        #                                                    initial_date__gte=initialDayQuarter, 
        #                                                    initial_date__lte=lastDayQuarter).values('id').values_list('id')


        # draft 
        #
        # Task.objects.values('goal')
        # for id in goal_ids:
        #    goal_task[id[0]] = Task.objects.values('task').annotate(count=Count('task')).filter(id=id[0])
        #
        # total_tasks = Task.objects.all().values_list('goal',flat=True).filter(goal=2) # tasks related to goal 2
        # 
        #
        
        # for id in qs_current_user_goals_quarter:
        #     goal_task[id[0]] = Task.objects.all().values_list('goal',flat=True).filter(goal=id[0])


        '''
        goal_task_finalized = {}
        goal_task_cancelled = {}
        goal_task_active    = {}
        goal_task_total     = {}

        qs_current_user_goals_quarter = Goal.objects.filter(accounts=1, 
                        initial_date__gte=initialDayQuarter, initial_date__lte=lastDayQuarter)
                        .values('id','goal').values_list('id','goal')

        for id, value in enumerate(qs_current_user_goals_quarter):
            goal_task_active[value[1]] = Task.objects.values('goal').order_by().annotate(task_goal_count=Count('goal')).filter(goal=value[0])

        goal, qs = zip(*goal_task_active.items())

        #for element in qs:
        #    for object in element:
        #        print(object)
        
        # get the count of values in a dictionary
        task_goal_count_values ={}
        for key_goal in goal:
            for element in goal_task_active[key_goal]:
                task_goal_count_values[key_goal] = element['task_goal_count']


        goal_task_active
        {'Finish the front end part of Telos': <QuerySet []>, 'A sample goal': <QuerySet [{'goal': 2, 'task_goal_count': 2}]>, 'Test for A1': <QuerySet []>}
        goal_task_finalized
        {'Finish the front end part of Telos': <QuerySet [{'goal': 1, 'task_goal_count': 3}]>, 'A sample goal': <QuerySet []>, 'Test for A1': <QuerySet []>}
        goal_task_total
        {'Finish the front end part of Telos': <QuerySet [{'goal': 1, 'task_goal_count': 3}]>, 'A sample goal': <QuerySet [{'goal': 2, 'task_goal_count': 2}]>, 'Test for A1': <QuerySet []>}
        finalized_goals, qs = zip(*goal_task_finalized.items())
        finalized_goals
        ('Finish the front end part of Telos', 'A sample goal', 'Test for A1')

        finalized_task_goal_count = {}
        for goal in finalized_goals:
        for element in goal_task_finalized[goal]:
        finalized_task_goal_count[goal] = element['task_goal_count']
        finalized_task_goal_count
        {'Finish the front end part of Telos': 3}


        total_goals, qs_total = zip(*goal_task_total.items())
        total_goals
        ('Finish the front end part of Telos', 'A sample goal', 'Test for A1')
        qs_total
        (<QuerySet [{'goal': 1, 'task_goal_count': 3}]>, <QuerySet [{'goal': 2, 'task_goal_count': 2}]>, <QuerySet []>)
        total_task_goal_count = {}
        for goal in total_goals:
        for element in goal_task_total[goal]:
        total_task_goal_count[goal] = element['task_goal_count']
        print(total_task_goal_count)
        print(finalized_task_goal_count)

        percentages_task_goals = {}
        for goal in total_goals:
        try:
             percentages_task_goals[goal] = (finalized_task_goal_count[goal]*100)/total_task_goal_count[goal]
        except:
             print("Key not found")
        '''
        #x_axis = list(qs_current_user_goals_quarter.values_list('goal')) #name of the goals to be displayed in the x axis

        print(x_axis, y_axis)
        # tasks -> goals
        #qs = Task.objects.filter(goal__in=goal_ids)
        # qs = Task.objects.filter(status='A

        # only the goals with finalized tasks are being displayed, fix this
        front_end_dictionary = {
            "labels_graph": x_axis,
            "values_graph": y_axis
        }
        return Response(front_end_dictionary)


@login_required
def create_task(request):
    '''You are passing the form TaskModel into the template, so it can render it.'''
    form_create = TaskModelForm(request.POST or None)
    goal = DropDownMenuGoalsForm(id = request.user.id)
    #category = DropDownMenuCategoriesForm(id = request.user.id)

    #Goal.objects.values_list('goal',flat=True).filter(accounts=User.objects.get(id=user_id),status='In Progress'))

    #print(goals_dropdownmenu)
    #username_id = None
    #if request.user.get_username():    
    #    username_id = User.objects.get(id=request.user.id)

    # Messy code but it works to get the goals id that will be used to insert in the goal_task_table
    select_goal_id = Goal.objects.values_list('id',flat=True).filter(goal=request.POST.get('goal', None))

    # task[0].task
    #user= User.objects.filter(username=username).values('score').values_list('score')[0][0]
    
    #select_goal_id = Goal.objects.filter(goal=request.POST.get('goal', None)).values('id').values_list('id',flat=True)[0][0]
    #new_val = select_goal_id[0].id

    for value in select_goal_id:
        new_val = value

    #select_category_id = Category.objects.values_list('id',flat=True).filter(category=request.POST.get('category',None))

    #for value in select_category_id:
    #    selected_category = value
    
    if form_create.is_valid():
        task = form_create.save(commit=True) # save the first task
        task.goal.add(new_val)  # associate the task with the goal by the id

        #obj.username = username_id # save the username_id in the task_task table
        task.save() 
        # Clean the form
        form_create = TaskModelForm()
        return redirect('/tasks/')
        
    template_name = 'task/formTask.html'
    # the form keyword gets all the data that will be passed along to the formCreate template
    context = {'form': form_create,
               #'category': category,
               'goal': goal
               }
    return render(request, template_name, context)


@login_required
def delete_task(request, id):
    '''Delete a task'''
    task = Task.objects.get(pk=id) # get the current points of the task
    if request.method == "POST":
        holder = User.objects.filter(id=request.user.id).values('score').values_list('score')[0][0] # get the current point of the user
        User.objects.filter(id=request.user.id).update(score=holder-float(task.points)) # subtract the total points minus the subtracted points
        task.delete() # delete the task from the db
    return redirect('/tasks/')

@login_required
def retrieve_all(request):
    '''Get the list of all tasks'''
    template_name = 'task/formRetrieval.html'
    
    goal_ids = []
    #user -> goal
    qs_current_user_goals = Goal.objects.filter(initial_date__gte='2020-03-15', initial_date__lte='2020-03-31', 
                            accounts=request.user.id).values('id').values_list('id')

    for value in qs_current_user_goals:
        goal_ids.append(value)
    
    # tasks ->  goals
    form = {'task_list': Task.objects.filter(goal__in=goal_ids)}
    
    return render(request, template_name, form)

@login_required
def update_task(request, id):
    '''Update a task'''
    task = Task.objects.get(pk=id)  # get the task id from the db
    form = TaskModelForm(request.POST or None, instance=task) # overwrite the task, do not create a new one

    if request.method == "GET":
        template_name = 'task/formTask.html'
        return render(request, template_name, {'form': form})

    # when the forms gets updated, the task disappears from the db
    elif request.method == "POST":
        if form.is_valid():
            holder = User.objects.filter(id=request.user.id).values('score').values_list('score')[0][0] # get the current point of the user
            if request.POST.get('status', None) == 'Finalized':
                User.objects.filter(id=request.user.id).update(score=holder+float(request.POST.get('points', None))) # get the points of the form with section points
            elif request.POST.get('status', None) == 'Cancelled':
                User.objects.filter(id=request.user.id).update(score=holder-float(request.POST.get('points', None))) # get the points of the form with section points
            #form.cleaned_data['username'] = request.user.id # doesn't work this line
            form.save()
            '''Below you need to update the username.id in the task_task table because if the task gets updated or cancelled then the username.id
               is erased because in the form there's no visible field to get the username id. The solution is not the cleanest but it works.'''
            
            '''The reason for the error django.model object has no attribute 'update' is that .get() returns an individual object and .update() only works on querysets, 
                such as what would be returned with .filter() instead of .get(). If you are using .get(), then .update() will not work.'''
            task.username=User.objects.get(id=request.user.id)
            task.save()
        return redirect('/tasks/')

@login_required
def view_previous_tasks(request):
    if request.method == "GET":
        template_name = 'task/no_retrieval_results/previous_tasks.html'
        form = DropDownMenuForm()
        return render(request, template_name, {'form': form})

    elif request.method == "POST":
        template_name = 'task/retrieval_results/previous_tasks.html'
        year = request.POST.get('select_year', None)
        week = request.POST.get('select_week', None)

        # Return only the initial date with 0 because the ending date can be obtained by adding 7 additional days
        initial_date, ending_date = get_start_end_date(year, week)

        goal_ids = []   
        qs_current_user_goals = Goal.objects.filter(initial_date__gte=initial_date, initial_date__lte=ending_date, 
                            accounts=request.user.id).values('id').values_list('id')

        for value in qs_current_user_goals:
            goal_ids.append(value)

        # Filter the data based on the initial date and active tasks
        # This qs cannot be commented because of the values_to_display_table
        qs = Task.objects.filter(goal__in = goal_ids)


        # there's an error when you start having different tasks, they are not counting

        qs_group_by = Task.objects.values(
            'category').annotate(count=Count('category')).filter(goal__in = goal_ids).order_by('count')

        keys_graph = list(qs_group_by.values_list('category'))
        values_graph = list(qs_group_by.values_list('count'))

        values_to_display_table = list(qs.values_list())

        front_end_dictionary = {
            "year": year,
            "week": week,
            "table_results": values_to_display_table,
            "labels_graph": keys_graph,
            "values_graph": values_graph
        }

        # serialize the dictionary
        converted_front_end_dictionary = {'converted_front_end_dictionary': json.dumps(
            front_end_dictionary, indent=4, sort_keys=True, default=str)}

        return render(request, template_name, converted_front_end_dictionary)

@login_required
def view_previous_tasks_monthly(request):
    if request.method == "GET":
        template_name = 'task/no_retrieval_results/previous_tasks_monthly.html'
        form = DropDownMenuMonthsForm()
        return render(request, template_name, {'form': form})

    elif request.method == "POST":
        template_name = 'task/retrieval_results/previous_tasks_monthly.html'
        year = request.POST.get('select_year', None)
        month = request.POST.get('select_month', None)

        # Return only the initial date with 0 because the ending date can be obtained by adding 7 additional days
        initial_date, ending_date = get_start_end_date_monthly(year, month)


        goal_ids = []   
        qs_current_user_goals = Goal.objects.filter(initial_date__gte=initial_date, initial_date__lte=ending_date, 
                            accounts=request.user.id).values('id').values_list('id')

        for value in qs_current_user_goals:
            goal_ids.append(value)

        # Filter the data based on the initial date and active tasks
        # This qs cannot be commented because of the values_to_display_table
        qs = Task.objects.filter(goal__in = goal_ids)


        qs_group_by = Task.objects.values(
            'category').annotate(count=Count('category')).filter(goal__in = goal_ids).order_by('count')

        keys_graph = list(qs_group_by.values_list('category'))
        values_graph = list(qs_group_by.values_list('count'))

        values_to_display_table = list(qs.values_list())

        front_end_dictionary = {
            "year": year,
            "month": month,
            "table_results": values_to_display_table,
            "labels_graph": keys_graph,
            "values_graph": values_graph
        }

        # serialize the dictionary
        converted_front_end_dictionary = {'converted_front_end_dictionary': json.dumps(
            front_end_dictionary, indent=4, sort_keys=True, default=str)}

        return render(request, template_name, converted_front_end_dictionary)

@login_required
def view_previous_tasks_yearly(request):
    if request.method == "GET":
        template_name = 'task/no_retrieval_results/previous_tasks_yearly.html'
        form = DropDownMenuYearsForm()
        return render(request, template_name, {'form': form})

    elif request.method == "POST":
        template_name = 'task/retrieval_results/previous_tasks_yearly.html'
        year = request.POST.get('select_year', None)

        # Return only the initial date with 0 because the ending date can be obtained by adding 7 additional days
        initial_date, ending_date = get_start_end_date_yearly(year)
        
        goal_ids = []   
        qs_current_user_goals = Goal.objects.filter(initial_date__gte=initial_date, initial_date__lte=ending_date, 
                            accounts=request.user.id).values('id').values_list('id')

        for value in qs_current_user_goals:
            goal_ids.append(value)

        # Filter the data based on the initial date and active tasks
        # This qs cannot be commented because of the values_to_display_table
        qs = Task.objects.filter(goal__in = goal_ids)


        qs_group_by = Task.objects.values(
            'category').annotate(count=Count('category')).filter(goal__in = goal_ids).order_by('count')


        keys_graph = list(qs_group_by.values_list('category'))
        values_graph = list(qs_group_by.values_list('count'))

        values_to_display_table = list(qs.values_list())

        front_end_dictionary = {
            "year": year,
            "table_results": values_to_display_table,
            "labels_graph": keys_graph,
            "values_graph": values_graph
        }

        # serialize the dictionary
        converted_front_end_dictionary = {'converted_front_end_dictionary': json.dumps(
            front_end_dictionary, indent=4, sort_keys=True, default=str)}

        return render(request, template_name, converted_front_end_dictionary)


def get_start_end_date(year, week):
    '''Given the year and week, return the first and last day of the given week and year.
       The first day is Sunday and last day is Saturday'''

    year = int(year)
    week = int(week)

    d = date(year, 1, 1)
    # patch to fix the problem of the retrieval of data for the first weeks of the year
    dlt = timedelta(days=(week - 1) * 7)

    if (d.weekday() <= 3):
        d = d - timedelta(d.weekday())
    else:
        # this line  d = d + timedelta(6 - d.weekday()) indicates to start in Sunday and end in Saturday
        # but it breaks when the retrieval is during the first weeks of the year, so we have to change the code
        # back to d = d + timedelta(7 - d.weekday())
        d = d + timedelta(7 - d.weekday())
    return d + dlt, d + dlt + timedelta(days=6)


def get_start_end_date_monthly(year, month):

    initial_day = str("01")  # first day of month as a zero padded decimal number
    ending_day  = str(calendar.monthrange(int(year), int(month))[1])  # get the last day of the month

    # Get only the date values, do not consider the time values
    initial_date = str(datetime(int(year), int(month), int(initial_day))).split(" ")[0]
    ending_date  = str(datetime(int(year), int(month), int(ending_day))).split(" ")[0]

    return initial_date, ending_date



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