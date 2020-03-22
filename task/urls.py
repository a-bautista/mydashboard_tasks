from django.urls import path
# import the component task
from .views import (create_task, delete_task, update_task,
                    view_previous_tasks, view_previous_tasks_monthly, view_previous_tasks_yearly, retrieve_all, main_dashboard,
                    Dashboard_Categories_Month, Dashboard_Status_Month,
                    Dashboard_Tasks_Week, Dashboard_Goals_Quarter, Dashboard_Goals_Year, Dashboard_Goals_Status_Task)

# Because I am redirecting the root address to the Task application, I need to include the task in the URL, so it gets defined in the lines below

urlpatterns = [
    path('', main_dashboard, name='main_dashboard'), # main dashboard page
    path('dashboard_categories_month', Dashboard_Categories_Month.as_view()), # load this view in the main page
    path('dashboard_status_month', Dashboard_Status_Month.as_view()),         # load this view in the main page
    path('dashboard_points_week', Dashboard_Tasks_Week.as_view()),
    path('dashboard_goals_quarter', Dashboard_Goals_Quarter.as_view()),
    path('dashboard_goals_year', Dashboard_Goals_Year.as_view()),
    path('dashboard_goals_status_task', Dashboard_Goals_Status_Task.as_view()),
    path('list/', retrieve_all),
    path('new/', create_task, name='create_task'),
    path('update/<int:id>/', update_task, name='update_task'),
    path('delete/<int:id>/', delete_task, name='delete_task'),
    path('previous_tasks/', view_previous_tasks),
    path('previous_tasks_monthly/', view_previous_tasks_monthly),
    path('previous_tasks_yearly/', view_previous_tasks_yearly)
]
