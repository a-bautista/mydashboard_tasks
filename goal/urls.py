from django.urls import path
# import the component task
from .views import (    
                        create_goal, 
                        update_goal,
                        delete_goal,
                        #view_previous_goals_quarter, 
                        #view_previous_goals_yearly, 
                        retrieve_all, 
                        #main_dashboard
                    )

# Because I am redirecting the root address to the Task application, 
# I need to include the goal in the URL, so it gets defined in the lines below

urlpatterns = [
    #path('', main_dashboard, name='main_dashboard'), # main dashboard page
    path('list/', retrieve_all),
    path('new/', create_goal, name='create_goal'),
    path('update/<int:id>/', update_goal, name='update_goal'),
    path('delete/<int:id>/', delete_goal, name='delete_goal'),
    #path('previous_goals_quarterly/', view_previous_goals_quarterly),
    #path('previous_goals_yearly/', view_previous_goals_yearly)
]
