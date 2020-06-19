from datetime import date, datetime, timedelta, time
from django.views.generic import View
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count, TextField
from django.db.models.functions import Cast
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .forms import TaskModelForm, DropDownMenuForm, DropDownMenuMonthsForm, DropDownMenuYearsForm, DropDownMenuGoalsForm, DropDownMenuSelectedGoalsForm, DropDownMenuCategoryForm, DropDownMenuSelectedCategoryForm
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Task, Goal, Category # I can use Goal here because I already imported this model in models.py/task
from user_profile.models import Profile # I need to use this syntax because I haven't imported this model on anywhere else
import json, calendar
from decimal import Decimal
from collections import Counter

from django.contrib.auth import get_user_model
User = get_user_model()


@login_required
def main_dashboard(request):
    username = None
    if request.user.get_username():
        username = request.user.username
  
    score   = round(Profile.objects.filter(user_id=request.user.id).values('score').values_list('score')[0][0])    
    week    = date.today().isocalendar()[1]
    month   = datetime.today().month
    year    = datetime.today().year
    quarter = (month-1)//3+1
    
    initialDayQuarter = datetime(year, 3 * quarter - 2, 1)
    lastDayQuarter    = datetime(year, (3 * quarter)%12+1, 1) + timedelta(days=-1)

    context = { "points": score, "month": datetime.now().strftime("%B"), "week": week, 
                "initial_date_quarter": initialDayQuarter, "lastDayQuarter":lastDayQuarter,
                "current_date": date.today() } # display the current points, current month, current week
    return render(request, 'task/mainDashboard.html', context)


class Dashboard_Categories_Month(APIView):

    def get(self, request, *args, **kwargs):
        year = date.today().year
        month = date.today().month
        
        # get the categories from users
        qs = Category.objects.filter(accounts=request.user.id).values('id').values_list('id',flat=True)
        category_id = []

        for c in qs:
            category_id.append(c)

        # do a reference of categories and tasks
        task_count = Task.objects.filter(category__in=category_id).distinct()

        new_list = []
        # append only the categories of each user
        for t in task_count:
            new_list.append(list(t.category.values('category').values_list('category', flat=True))[0])

        # count the categories
        results = Counter(new_list)

        keys_graph = results.keys()
        values_graph = results.values()

        front_end_dictionary = {
            "labels_graph": keys_graph,
            "values_graph": values_graph
        }
        return Response(front_end_dictionary)


class Dashboard_Status_Month(APIView):

    def get(self, request, *args, **kwargs):
        year = date.today().year
        month = date.today().month
        initial_date_year, ending_date_year = get_start_end_date_yearly(year)
        #initial_date, ending_date = get_start_end_date_monthly(year, month)
        
        quarter   = (month-1)//3+1
        initialDayQuarter = datetime(year, 3 * quarter - 2, 1)
        lastDayQuarter    = datetime(year, (3 * quarter)%12+1, 1) + timedelta(days=-1)

        goal_ids = []   
        qs_current_user_goals = Goal.objects.filter(initial_date__gte=initial_date_year, initial_date__lte=ending_date_year, 
                            accounts=request.user.id).values('id').values_list('id')


        for value in qs_current_user_goals:
            goal_ids.append(value)


        # there's an error when you start having different tasks, they are not counting, really?
        qs_group_by = Task.objects.values(
            'status').annotate(count=Count('status')).filter(goal__in = goal_ids, 
            initial_date__gte=initialDayQuarter, initial_date__lte=lastDayQuarter).order_by('count')


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
                task.points = (task.points*standard_increase_points)
                task.life_task = task.life_task - 1
            elif (datetime.now()-datetime.combine(task.initial_date,time())) >= timedelta(days=14) and (datetime.now()-datetime.combine(task.initial_date,time())) < timedelta(days=21) and task.life_task == 2:
                task.points = (task.points*standard_increase_points)
                task.life_task = task.life_task - 1
            elif (datetime.now()-datetime.combine(task.initial_date,time())) >= timedelta(days=21) and (datetime.now()-datetime.combine(task.initial_date,time())) < timedelta(days=28) and task.life_task == 1:
                task.points = (task.points*last_increase_points)
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
                holder = Profile.objects.filter(user_id=request.user.id).values('score').values_list('score')[0][0] # get the points of the form with section points
                Profile.objects.filter(user_id=request.user.id).update(score=holder-int(task.points)) # subtract the points from the general score
            task.save()
  
        x_axis    = list(qs.values_list('task'))
        temp_list = qs.values_list('points')
        
        # display only rounded values
        y_axis = [round(val[0]) for val in temp_list ]

        front_end_dictionary = {
            "labels_graph": x_axis,
            "values_graph": y_axis
        }
        return Response(front_end_dictionary)


class Dashboard_Goals_Quarter(APIView):
    ''' Display all the quarterly goals and indicate the % of progress in each one once they have been finalized. '''
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
        x_axis = None
        y_axis = None

        # goals -> users
        qs_current_user_goals_quarter = Goal.objects.filter(accounts=request.user.id, 
                                                            initial_date__gte=initialDayQuarter, 
                                                            expiration_date__lte=lastDayQuarter,
                                                            status='In Progress').values('id','goal').values_list('id','goal')
        
        for id, value in enumerate(qs_current_user_goals_quarter):
            goal_task_finalized[value[1]] = Task.objects.values('goal').order_by().annotate(task_goal_count=Count('goal')).filter(goal=value[0], status='Finalized')
            goal_task_total[value[1]] = Task.objects.values('goal').order_by().annotate(task_goal_count=Count('goal')).filter(goal=value[0])


        if goal_task_finalized and goal_task_total:

            finalized_goals, qs_finalized = zip(*goal_task_finalized.items())
            total_goals,     qs_total     = zip(*goal_task_total.items())

            
            for goal in finalized_goals:
                for element in goal_task_finalized[goal]:
                    finalized_task_goal_count[goal] = element['task_goal_count']

            for goal in total_goals:
                for element in goal_task_total[goal]:
                    total_task_goal_count[goal] = element['task_goal_count']

            
            for goal in total_goals:
                try:
                    percentages_task_goals[goal] = round((finalized_task_goal_count[goal]*100)/total_task_goal_count[goal])
                except:
                    # assign the goal that doesn't have any finalized task to 0, so you can visualize it in the graph
                    percentages_task_goals[goal] = 0

            #print(percentages_task_goals)
            x_axis, y_axis = zip(*percentages_task_goals.items())

            #qs_current_user_goals_quarter = Goal.objects.filter(accounts=1, 
            #                                                    initial_date__gte=initialDayQuarter, 
            #                                                    initial_date__lte=lastDayQuarter).values('id').values_list('id')

            
            #x_axis = list(qs_current_user_goals_quarter.values_list('goal')) #name of the goals to be displayed in the x axis

            #print(x_axis, y_axis)
            # tasks -> goals
            #qs = Task.objects.filter(goal__in=goal_ids)
            # qs = Task.objects.filter(status='A

        # only the goals with finalized tasks are being displayed, fix this
        front_end_dictionary = {
            "labels_graph": x_axis,
            "values_graph": y_axis,
            "legend":['Active','Finalized','Cancelled']
        }
        return Response(front_end_dictionary)


class Dashboard_Goals_Status_Task(APIView):
    ''' Display all the quarterly goals and indicate the % of progress in each one once they have been finalized. '''
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
        goal_task_cancelled = {}
        goal_task_active    = {}
        goal_task_total     = {}


        finalized_task_goal_count = {}
        cancelled_task_goal_count = {}
        active_task_goal_count    = {}

        goal_status_count         = {}

        goal_ids = []   
        cancelled = []
        active =[]
        finalized = []

        y_axis = []
        x_axis = []
        # goals -> users
        qs_current_user_goals_quarter = Goal.objects.filter(accounts=request.user.id, 
                                                            initial_date__gte=initialDayQuarter, 
                                                            expiration_date__lte=lastDayQuarter,
                                                            status='In Progress').values('id','goal').values_list('id','goal')
        
        #print(qs_current_user_goals_quarter)
        for id, value in enumerate(qs_current_user_goals_quarter):
            goal_task_total[value[1]]     = Task.objects.values('goal').order_by().annotate(task_goal_count=Count('goal')).filter(goal=value[0])
            goal_task_finalized[value[1]] = Task.objects.values('goal').order_by().annotate(task_goal_count=Count('goal')).filter(goal=value[0], status='Finalized')
            goal_task_active[value[1]]    = Task.objects.values('goal').order_by().annotate(task_goal_count=Count('goal')).filter(goal=value[0], status='Active')
            goal_task_cancelled[value[1]] = Task.objects.values('goal').order_by().annotate(task_goal_count=Count('goal')).filter(goal=value[0], status='Cancelled')   


        if goal_task_total and goal_task_finalized and goal_task_active and goal_task_cancelled:
            total_goals,     qs_total     = zip(*goal_task_total.items())
            finalized_goals, qs_finalized = zip(*goal_task_finalized.items())
            active_goals,    qs_active    = zip(*goal_task_active.items())
            cancelled_goals, qs_active    = zip(*goal_task_cancelled.items())  


            for goal in finalized_goals:
                for element in goal_task_finalized[goal]:
                    finalized_task_goal_count[goal] = element['task_goal_count']

            
            for goal in active_goals:
                for element in goal_task_active[goal]:
                    active_task_goal_count[goal] = element['task_goal_count']

            for goal in cancelled_goals:
                for element in goal_task_cancelled[goal]:
                    cancelled_task_goal_count[goal] = element['task_goal_count']

            
            # populate the dictionary with empty lists to store the count of active, cancelled and finalized goals
            for goal in total_goals:
                goal_status_count[goal]=goal_status_count.get(goal,[])

            
            for goal in total_goals:
                try:
                    goal_status_count[goal].append(finalized_task_goal_count[goal])
                except:
                    # assign the goal that doesn't have any finalized task to 0, so you can visualize it in the graph
                    goal_status_count[goal].append(0)
                    

            for goal in total_goals:
                try:
                    goal_status_count[goal].append(active_task_goal_count[goal])
                except:
                    # assign the goal that doesn't have any finalized task to 0, so you can visualize it in the graph
                    goal_status_count[goal].append(0)
            
            for goal in total_goals:
                try:
                    goal_status_count[goal].append(cancelled_task_goal_count[goal])
                except:
                    # assign the goal that doesn't have any finalized task to 0, so you can visualize it in the graph
                    goal_status_count[goal].append(0)


            x_axis, temp_y_axis = zip(*goal_status_count.items())
            
            for inner_list in temp_y_axis:
                for i in range(len(inner_list)):
                    if i==0:
                        cancelled.append(inner_list[i])
                    elif i == 1:
                        active.append(inner_list[i])
                    elif i == 2:
                        finalized.append(inner_list[i])
            
            
            y_axis.append(cancelled)
            y_axis.append(active)
            y_axis.append(finalized)
       
        # only the goals with finalized tasks are being displayed, fix this
        front_end_dictionary = {
            "labels_graph": x_axis,
            "values_graph": y_axis,
            "legend": ['Finalized','Active','Cancelled']
        }
        return Response(front_end_dictionary)


class Dashboard_Long_Medium_Term_Goals(APIView):
    ''' Display all the medium term goals and indicate the % of progress in each one once they have been finalized. '''
    def get(self, request, *args, **kwargs):

        '''Show only the results of the logged in user'''
        year  = date.today().year
        initial_date, ending_date = get_start_end_date_yearly(year)

        goal_task_finalized = {}
        goal_task_total     = {}

        finalized_task_goal_count = {}
        total_task_goal_count     = {}
        percentages_task_goals    = {}

        x_axis = None
        y_axis = None

        status_to_exclude = ['Cancelled','Not completed']
        goal_type = ['Medium','Long']

        goal_ids = []   
        # goals -> users
        qs_current_user_goals_quarter = Goal.objects.filter(accounts=request.user.id, goal_type__in=goal_type).exclude(status__in=status_to_exclude).values('id','goal').values_list('id','goal')

        for id, value in enumerate(qs_current_user_goals_quarter):
            goal_task_finalized[value[1]] = Task.objects.values('goal').order_by().annotate(task_goal_count=Count('goal')).filter(goal=value[0], status='Finalized')
            goal_task_total[value[1]] = Task.objects.values('goal').order_by().annotate(task_goal_count=Count('goal')).filter(goal=value[0])

        # if the dictionaries are not empty - fix for displaying the graphs when a user logs in for the first time
        if goal_task_finalized and goal_task_total:
            finalized_goals, qs_finalized = zip(*goal_task_finalized.items())
            total_goals,     qs_total     = zip(*goal_task_total.items())

        
            for goal in finalized_goals:
                for element in goal_task_finalized[goal]:
                    finalized_task_goal_count[goal] = element['task_goal_count']

            for goal in total_goals:
                for element in goal_task_total[goal]:
                    total_task_goal_count[goal] = element['task_goal_count']

            
            for goal in total_goals:
                try:
                    percentages_task_goals[goal] = round((finalized_task_goal_count[goal]*100)/total_task_goal_count[goal])
                except:
                    # assign the goal that doesn't have any finalized task to 0, so you can visualize it in the graph
                    percentages_task_goals[goal] = 0

            x_axis, y_axis = zip(*percentages_task_goals.items())            

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
    category = DropDownMenuCategoryForm(id=request.user.id)

    selected_goal = None
    selected_category = None

    # Messy code but it works to get the goals id that will be used to insert in the goal_task_table
    select_goal_id = Goal.objects.values_list('id',flat=True).filter(goal=request.POST.get('goal', None))

    for value in select_goal_id:
        selected_goal = value

    select_category_id = Category.objects.values_list('id',flat=True).filter(category=request.POST.get('category',None))

    for value in select_category_id:
        selected_category = value
    
    if form_create.is_valid():
        task = form_create.save(commit=True) # save the first task
        task.goal.add(selected_goal)  # associate the task with the goal by the id
        task.category.add(selected_category)
        task.save() 

        # Clean the form
        form_create = TaskModelForm()
        return redirect('/main/')
        
    template_name = 'task/formTask.html'
    # the form keyword gets all the data that will be passed along to the formCreate template
    context = {'form': form_create,
               'goal': goal,
               'category': category
               }
    return render(request, template_name, context)


@login_required
def delete_task(request, id):
    '''Delete a task'''
    task = Task.objects.get(pk=id) # get the current points of the task
    if request.method == "POST":
        holder = Profile.objects.filter(user_id=request.user.id).values('score').values_list('score')[0][0] # get the current point of the user
        Profile.objects.filter(user_id=request.user.id).update(score=holder-Decimal(task.points)) # subtract the total points minus the subtracted points
        task.delete() # delete the task from the db
    return redirect('/main/')

@login_required
def retrieve_all(request):
    '''Get the list of all tasks created during the quarter (you will focus only on the tasks of the current quarter).'''
    template_name = 'task/formRetrieval.html'
    status_goal = 'In Progress'
    status_task = 'Active'

    goal_ids       = []
    categories_ids = []

    qs_current_user_goals = Goal.objects.filter(accounts=request.user.id, 
                                                            status=status_goal).values('id').values_list('id')

    qs_current_user_categories = Category.objects.filter(accounts=request.user.id)

    # tasks ->  goals
    for goal in qs_current_user_goals:
        goal_ids.append(goal)

    # tasks -> categories
    for category in qs_current_user_categories:
        categories_ids.append(category)
    
    form = {'task_list': Task.objects.filter(goal__in=goal_ids, category__in=categories_ids, status=status_task).distinct()}
    
    return render(request, template_name, form)

@login_required
def update_task(request, id):
    '''Update a task'''
    task = Task.objects.get(pk=id)  # get the task id from the db

    # task.goal.values() allows me to see all the fields that are associated to the relationship
    initial_value_goal = task.goal.values_list('goal',flat=True)[0]
    
    # task.category.values() 
    initial_value_category = task.category.values_list('category',flat=True)[0]

    # overwrite the task, do not create a new one
    form = TaskModelForm(request.POST or None, instance=task) 

    # initialize the Goals dropdown menu
    goal = DropDownMenuSelectedGoalsForm(id = request.user.id, initial={'goal': initial_value_goal})

    # initialize the Category dropdown menu
    category = DropDownMenuSelectedCategoryForm(id = request.user.id, initial={'category': initial_value_category})

    if request.method == "GET":
        template_name = 'task/formTask.html'
        return render(request, template_name, {'form': form, 'goal':goal, 'category': category})

    # when the forms gets updated, the task disappears from the db
    elif request.method == "POST":
        if form.is_valid():
            holder = Profile.objects.filter(user_id=request.user.id).values('score').values_list('score')[0][0] # get the current point of the user                 

            # look for the previous id of the goal
            old_goal_id = task.goal.values_list('id',flat=True)[0]

            # look for the previous id of the category
            old_category_id = task.category.values_list('id', flat=True)[0]

            # look for the new id of the goal
            new_goal_id = Goal.objects.values_list('id',flat=True).filter(goal=request.POST.get('goal', None))[0]

            # look for the new id of the category
            new_category_id = Category.objects.values_list('id',flat=True).filter(category=request.POST.get('category', None))[0]

            if old_goal_id!=new_goal_id:

                # Associate the new goal to the current task
                # print("Associating the task with the new goal")
                task.goal.add(new_goal_id)

                # remove the old goal from the current task
                # print("Deleting the task with the new goal")
                task.goal.remove(old_goal_id)

            if old_category_id!= new_category_id:
                # Associate the new category to the current task
                # print("Associating the category with the new task")
                task.category.add(new_category_id)

                # Remove the old category from the current task
                # print("Removing the category from the new task")
                task.category.remove(old_category_id)
            
            # calculate the  points
            if request.POST.get('status', None) == 'Finalized':
                Profile.objects.filter(user_id=request.user.id).update(score=holder+Decimal(request.POST.get('points', None))) # get the points of the form with section points
            elif request.POST.get('status', None) == 'Cancelled':
                Profile.objects.filter(user_id=request.user.id).update(score=holder-Decimal(request.POST.get('points', None))) # get the points of the form with section points
            
            form.save()
            
            '''The reason for the error django.model object has no attribute 'update' is that .get() returns an individual object and .update() only works on querysets, 
               such as what would be returned with .filter() instead of .get(). If you are using .get(), then .update() will not work.'''

        return redirect('/main/')

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