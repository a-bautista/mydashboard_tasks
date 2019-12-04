from datetime import date, datetime, timedelta
from django.views.generic import View
from django.shortcuts import render, get_object_or_404
from .forms import TaskModelForm, DropDownMenuForm
import psycopg2
import json


class HomeView(View):
    def get(self, request, *args, **kwargs):
        my_title = "Telos App"
        # I had to configure the template dir in the settings of the app
        context = {"title": my_title}
        return render(request, 'task/home.html', context)


def create_task(request):
    '''You are passing the form TaskModel into the template, so it can render it.'''
    form_create = TaskModelForm(request.POST or None)
    if form_create.is_valid():
        # print(form.cleaned_data)
        # obj = Task.objects.create(**form.cleaned_data) grabs all the fields from the forms and stores them in the Task
        obj = form_create.save(commit=False)
        # obj = Task.objects.create(**form.cleaned_data)
        # you can do intermediate steps with the class based models
        # obj.responsible = form.cleaned_data.get('responsible') + "0"
        obj.save()
        # Reinitialize the form or clean it
        form = TaskModelForm()
    template_name = 'task/formCreate.html'

    # the form gets all the data that will be passed along
    context = {'form_create': form_create}
    return render(request, template_name, context)


def delete_task(request):
    template_name = 'task/delete.html'
    context = {'form': None}
    return render(request, template_name, context)


def update_task(request):
    template_name = 'task/update.html'
    context = {'form': None}
    return render(request, template_name, context)

# Ajax maybe?


'''
def view_tasks(request):
    template_name = 'task/tasks.html'
    dictionary_general = connection_db_postgresql()
    converted_dictionary_general = \
        {'converted_dictionary_general': json.dumps(dictionary_general)}
    # print(converted_dictionary_general)
    return render(request, template_name, converted_dictionary_general)
'''


def view_previous_tasks(request):
    if request.method == "GET":
        template_name = 'task/no_retrieval_results/previous_tasks.html'
        form = DropDownMenuForm()
        return render(request, template_name, {'form': form})

    elif request.method == "POST":
        template_name = 'task/retrieval_results/previous_tasks.html'
        year = request.POST.get('select_year', None)
        week = request.POST.get('select_week', None)
        values_graph = ""
        keys_graph = ""

        option = 0
        # Return only the initial date with 0 because the ending date can be obtained by adding 7 additional days
        initial_date = get_start_end_date(year, week)[0]
        beginning_datetime_format, ending_datetime_format = conversion_string_to_datetime(
            initial_date)

        general_dictionary = connection_db_postgresql(option, beginning_datetime_format,
                                                      ending_datetime_format)

        option = 1
        values_to_display_graph_dict = connection_db_postgresql(
            option, beginning_datetime_format, ending_datetime_format)

        # separate the dictionary into lists of keys and values
        # patch 0.0.1
        # Verify if you have an empty list. If you do then you will get an error when trying to create a dictionary based on empty list values
        if len(values_to_display_graph_dict) != 0:
            keys_graph, values_graph = zip(
                *values_to_display_graph_dict.items())

        values_to_display_table = get_values_table(general_dictionary)

        front_end_dictionary = {
            "year": year,
            "week": week,
            "table_results": values_to_display_table,
            "labels_graph": keys_graph,
            "values_graph": values_graph
        }

        converted_front_end_dictionary = {'converted_front_end_dictionary': json.dumps(
            front_end_dictionary)}

        return render(request, template_name, converted_front_end_dictionary)


def conversion_string_to_datetime(initial_date):

    beginning_year = str(initial_date).split("-")[0]
    beginning_month = str(initial_date).split("-")[1]
    beginning_day = str(initial_date).split("-")[2]

    beginning_hour = 0
    beginning_minute = 0
    beginning_second = 0

    # conversion from string to datetime
    beginning_datetime_format = datetime(int(beginning_year), int(beginning_month),
                                         int(beginning_day), int(
        beginning_hour),
        int(beginning_minute), int(beginning_second))

    ending_datetime_format = beginning_datetime_format + timedelta(days=7)

    return beginning_datetime_format, ending_datetime_format


def list_of_queries(option, beginning_datetime_format, ending_datetime_format):
    '''We will store the queries in a dictionary and then loop through  '''
    options = {0: "select id, responsible, task, status, category, initial_date, ending_date from task_task where initial_date between '" +
               str(beginning_datetime_format) + "' and '" +
               str(ending_datetime_format) + "';",
               1: "select category, count(*) from task_task where initial_date between '" + str(beginning_datetime_format) + "' and '" +
               str(ending_datetime_format) + "' group by category;"}

    # fix this because it doesn't make much sense
    for i in range(len(options)):
        if option in options:
            query = options[option]
        else:
            query = ""
    return query

# this needs to be encrypted


def connect_db():
    connection = psycopg2.connect(host="localhost",
                                  database="mydashboard_tasks",
                                  user="postgres",
                                  password="Ab152211")
    return connection


def connection_db_postgresql(option, beginning_datetime_format, ending_datetime_format):

    temp_list = []  # ['1', 'Alejandro', 'Task 1', '2019-10-29', None, ';' ]
    keys_dict_list = []  # ['1', '2', '3']
    general_list = []  # ['1', 'Alejandro', 'Task 1', '2019-10-29', None, ';' , '2', 'Alejandro', 'Task 2', '2019-10-30', None, ';']
    values_dict_list = []  # ['Alejandro', 'Task 1', '2019-10-29', None]

    query = list_of_queries(option, beginning_datetime_format,
                            ending_datetime_format)
    connection = connect_db()

    cursor = connection.cursor()
    cursor.execute(query)
    records = cursor.fetchall()
    cursor.close()
    # Iterate through the tuple to retrieve the results from the query

    for element in records:
        # get the ID of the task and store it in keys_dict_list
        keys_dict_list.append(element[0])
        # skip the first element 0 and start on the element 1 because I already got the IDs of each task in the list keys_dict_list
        for tuple_value in element[1:]:
            general_list.append(str(tuple_value))
        general_list.append(';')

    # print(records)
    # print("These are the values of the general list: \n")
    # print(general_list)

    for element in general_list:
        if element != ';':
            # Add each new element into a temporary list in order to display each task based on its ID.
            temp_list.append(element)
        else:
            # If the element is equal to ; then attach each new list into the another list that will hold
            # all the temporary lists, i.e., [[],[]]
            values_dict_list.append(temp_list)
            # print(temp_list)
            temp_list = []

    # print("The values of dict list:\n")
    # print(values_dict_list)

    # Based on 2 lists, create a dictionary
    # general_dictionary = {1: [], 2:[], 3:[]}
    general_dictionary = dict(zip(keys_dict_list, values_dict_list))

    print("These are the values of the general dictionary:")
    print(general_dictionary)
    print("\n")

    return general_dictionary


def get_values_table(general_dictionary):
    '''You need a list of lists to be able to see the results in the data tables.'''

    list_of_values = []
    values_to_display_table = []
    # iterate over a dictionary of lists {id: [1,2], responsible: [Alejandro Bautista Ramos, Alejandro Bautista Ramos]}
    for index, value in general_dictionary.items():
        for value_in_list in value:
            # print(value_in_list)
            list_of_values.append(value_in_list)
        values_to_display_table.append(list_of_values)
        # clean the list to attach the next results
        list_of_values = []
    return values_to_display_table


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
