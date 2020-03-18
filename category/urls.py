from django.urls import path
# import the component task
from .views import (    
                        create_category, 
                    )

# Because I am redirecting the root address to the Task application, 
# I need to include the goal in the URL, so it gets defined in the lines below

urlpatterns = [
    path('new/', create_category, name='create_category'),
]