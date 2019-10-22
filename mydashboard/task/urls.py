from django.urls import path
# import the component dashboard
from .views import (create_task,
                   delete_task,
                   update_task)

urlpatterns = [
    path('create/', create_task),
    path('update/', update_task),
    path('delete/', delete_task),
]
