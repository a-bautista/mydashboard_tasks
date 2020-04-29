"""mydashboard URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include, re_path

#import the URLs from the home app
from home.views import index
from task.views import (main_dashboard, Dashboard_Categories_Month, 
                Dashboard_Status_Month, Dashboard_Tasks_Week, Dashboard_Goals_Quarter, 
                Dashboard_Goals_Year, Dashboard_Goals_Status_Task)


from accounts import views as user_views

'''You can import the login/logout functionalities as template views in this file or you can customize them but you will have 
    to import them in your views.py file. '''
from django.contrib.auth import views as auth_views # we won't be using this because we have customized our Users model

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('register/', user_views.register, name='register'),
    path('profile/', user_views.profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='accounts/logout.html'), name='logout'), # template view for logout
    path('main/', main_dashboard, name='main_dashboard'), # when you reach dashboard, go directly to look for the urls from the Task application
    path('tasks/', include('task.urls')),
    path('goals/', include('goal.urls')),

    path('main/dashboard_categories_month', Dashboard_Categories_Month.as_view()), # load this view in the main page
    path('main/dashboard_status_month', Dashboard_Status_Month.as_view()),         # load this view in the main page
    path('main/dashboard_points_week', Dashboard_Tasks_Week.as_view()),
    path('main/dashboard_goals_quarter', Dashboard_Goals_Quarter.as_view()),
    path('main/dashboard_goals_year', Dashboard_Goals_Year.as_view()),
    path('main/dashboard_goals_status_task', Dashboard_Goals_Status_Task.as_view()),
]
