from django.urls import path
# import the component task
from .views import (create_task, delete_task, update_task,
                    view_previous_tasks, view_previous_tasks_monthly, view_previous_tasks_yearly, retrieve_all, main_dashboard)

# Because I am redirecting the root address to the Task application, I need to include the task in the URL, so it gets defined in the lines below

urlpatterns = [
    path('list/', retrieve_all),
    path('new/', create_task, name='create_task'),
    path('update/<int:id>/', update_task, name='update_task'),
    path('delete/<int:id>/', delete_task, name='delete_task'),
    path('previous_tasks/', view_previous_tasks),
    path('previous_tasks_monthly/', view_previous_tasks_monthly),
    path('previous_tasks_yearly/', view_previous_tasks_yearly)
]
