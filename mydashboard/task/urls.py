from django.urls import path
# import the component task
from .views import (create_task
                    ,delete_task
                    ,update_task
                    ,view_tasks)

urlpatterns = [
    path('create/', create_task),
    path('update/', update_task),
    path('delete/', delete_task),
    path('tasks/',  view_tasks)
]
