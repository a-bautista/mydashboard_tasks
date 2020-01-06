from datetime import date, datetime, timedelta, time
from django.views.generic import View
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count
from .forms import TaskModelForm, DropDownMenuForm, User_PointsForm, DropDownMenuMonthsForm, DropDownMenuYearsForm
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Task, User_Points
import json, calendar


def home(request):
    user_points = User_Points.objects.filter(id=1).values('points').values_list('points')[0][0] # get the current values of your db
    week = date.today().isocalendar()[1]
    context = { "points": user_points, "month": datetime.now().strftime("%B"), "week": week } # display the current points, current month, current week
    return render(request, 'task/home.html', context)

class Dashboard_Categories_Month(APIView):

    def get(self, request, *args, **kwargs):
        year = date.today().year
        month = date.today().month
        initial_date, ending_date = get_start_end_date_monthly(year, month)

        qs_group_by = Task.objects.values(
            'category').annotate(count=Count('category')).filter(initial_date__gte=initial_date, initial_date__lte=ending_date)

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

        qs_group_by = Task.objects.values(
            'status').annotate(count=Count('status')).filter(initial_date__gte=initial_date, initial_date__lte=ending_date)

        keys_graph = list(qs_group_by.values_list('status'))
        values_graph = list(qs_group_by.values_list('count'))
        front_end_dictionary = {
            "labels_graph": keys_graph,
            "values_graph": values_graph
        }
        return Response(front_end_dictionary)


class Dashboard_Tasks_Week(APIView):

    def get(self, request, *args, **kwargs):
        task = Task.objects.all()
        year = date.today().year
        week = date.today().isocalendar()[1]

        # Return only the initial date with 0 because the ending date can be obtained by adding 7 additional days
        #initial_date, ending_date = get_start_end_date(year, week)

        qs = Task.objects.values('task','points').filter(status='Active')
        
        id = list(qs.values_list('id'))
        points = list(qs.values_list('points'))
        initial_dates = list(qs.values_list('initial_date'))

        #set a flag to indicate that the task has been already updated
        # update the points based on the number of days that each task has been active
        '''
        for index, value in enumerate(initial_dates):
            if (datetime.combine(value[0],time())+ timedelta(days=7)) - datetime.combine(value[0],time()) == 7:
                points[index][0] = (points[index][0])* 1.25
                print("was it here?")
            elif (datetime.combine(value[0],time())+ timedelta(days=14)) - datetime.combine(value[0],time()) == 14:
                points[index][0] = (points[index][0])* 1.25
                print("was it here?")
            elif (datetime.combine(value[0],time())+ timedelta(days=21)) - datetime.combine(value[0],time()) == 21:
                points[index][0] = (points[index][0])* 1.25
                print("was it here?")
            elif (datetime.combine(value[0],time())+ timedelta(days=28)) - datetime.combine(value[0],time()) == 28:
                points[index][0] = (points[index][0])* 1.50
                print("was it here?")
            elif (datetime.combine(value[0],time())+ timedelta(days=28)) - datetime.combine(value[0],time()) == 35:
                # deactivate task and subtract all the points 
                points[index][0] = (points[index][0])* 1.50
                print("was it here?")
        
        for index, value in enumerate(id):
            task = Task.objects.filter(id=value[0])
            task.update(points=points[index][0])
        '''

        # get all the active tasks
        # if current task week < (current task week + 1 week)
            # increase points by 25%
        # else if current task week < (current task week + 2 weeks)
            # increase points by another 25%
        # else if current task week < (current task week + 3 weeks)
            # increase points by another 25%
        # else if current task week < (current task week + 4 weeks)
            # increase points by another 50%
        # else if current task week < (current task week + 5 weeks)
            # update the status of the task to cancelled and decrease the total points from the total score

        x_axis = list(qs.values_list('task'))
        y_axis = list(qs.values_list('points'))

        front_end_dictionary = {
            "labels_graph": x_axis,
            "values_graph": y_axis
        }
        return Response(front_end_dictionary)


def create_task(request):
    '''You are passing the form TaskModel into the template, so it can render it.'''
    form_create = TaskModelForm(request.POST or None)
    if form_create.is_valid():
        # print(form.cleaned_data)
        # obj = Task.objects.create(**form.cleaned_data) grabs all the fields from the forms and stores them in the Task
        obj = form_create.save()
        # The code from below allows us to do some intermediate steps to the data before storing them into the db
        #obj = form_create.save(commit=False)
        # obj = Task.objects.create(**form.cleaned_data)
        # you can do intermediate steps with the class based models
        #obj.points = form_create.cleaned_data.get('points')
        obj.save()
        # Clean the form
        form_create = TaskModelForm()
    template_name = 'task/formTask.html'
    # the form keyword gets all the data that will be passed along to the formCreate template
    context = {'form': form_create}
    return render(request, template_name, context)


def delete_task(request, id):
    '''Delete a task'''
    task = Task.objects.get(pk=id)
    user_points = User_Points.objects.filter(id=1) # get our only user from the db
    if request.method == "POST":
        holder = int(list(User_Points.objects.filter(id=1).values('points').values_list('points'))[0][0]) # get the current point of the task
        user_points.update(points=holder-int(task.points)) # subtract the total points minus the subtracted points
        task.delete() # delete the task from the db
    return redirect('/task/tasks/')


def retrieve_all(request):
    '''Get the list of all tasks'''
    template_name = 'task/formRetrieval.html'
    form = {'task_list': Task.objects.all()}
    return render(request, template_name, form)


def update_task(request, id):
    '''Update a task'''
    task = Task.objects.get(pk=id)  # get the task id from the db
    #user = User_Points.objects.get(pk=1)
    # overwrite the task, do not create a new one
    form = TaskModelForm(request.POST or None, instance=task)
    #user_points = User_PointsForm(request.POST or None, instance=user)
    user_points = User_Points.objects.filter(id=1) # get our only user from the db

    if request.method == "GET":
        template_name = 'task/formTask.html'
        return render(request, template_name, {'form': form})

    elif request.method == "POST":
        if form.is_valid():
            if request.POST.get('status', None) == 'Finalized':
                # extract the values from the qs and convert it to int, so you can add those values to the counter of points
                holder = int(list(User_Points.objects.filter(id=1).values('points').values_list('points'))[0][0])
                user_points.update(points=holder+int(request.POST.get('points', None))) # get the points of the form with section points
            elif request.POST.get('status', None) == 'Cancelled':
                # extract the values from the qs and convert it to int, so you can subtract those values to the counter of points
                holder = int(list(User_Points.objects.filter(id=1).values('points').values_list('points'))[0][0])
                user_points.update(points=holder-int(request.POST.get('points', None))) # get the points of the form with section points
            form.save()
        return redirect('/task/tasks/')


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
        #ending_date = initial_date + timedelta(days=6)
        #print(ending_date)

        # Filter the data based on the initial date and active tasks
        # This qs cannot be commented because of the values_to_display_table
        qs = Task.objects.filter(
            initial_date__gte=initial_date, initial_date__lte=ending_date)

        qs_group_by = Task.objects.values(
            'category').annotate(count=Count('category')).filter(initial_date__gte=initial_date, initial_date__lte=ending_date)

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
        qs = Task.objects.filter(
            initial_date__gte=initial_date, initial_date__lte=ending_date)

        qs_group_by = Task.objects.values(
            'category').annotate(count=Count('category')).filter(initial_date__gte=initial_date, initial_date__lte=ending_date)

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
        qs = Task.objects.filter(
            initial_date__gte=initial_date, initial_date__lte=ending_date)

        qs_group_by = Task.objects.values(
            'category').annotate(count=Count('category')).filter(initial_date__gte=initial_date, initial_date__lte=ending_date)

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


<<<<<<< HEAD
=======
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
>>>>>>> f99b684... Telos 1.1.0: Added the feature to see tasks by months and years.
