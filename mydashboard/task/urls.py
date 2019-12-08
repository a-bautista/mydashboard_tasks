from django.urls import path
# import the component task
from .views import (create_task, delete_task, update_task,
                    view_previous_tasks, retrieve_all)

urlpatterns = [
    path('tasks/', retrieve_all),
    path('new/', create_task, name='create_task'),
    path('update/<int:id>/', update_task, name='update_task'),
    path('delete/<int:id>/', delete_task, name='delete_task'),
    path('previous_tasks/', view_previous_tasks)
]
