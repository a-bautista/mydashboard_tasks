from django.urls import path
# import the component dashboard
from .views import (create_task,
                   delete_task,
                   update_task)

urlpatterns = [
    path('task-create/', create_task),
    path('task-update/', update_task),
    path('task-delete/', delete_task),
]
