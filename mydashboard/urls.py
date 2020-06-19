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
from django.urls import path, include
from django.conf.urls import url 

#import the URLs from the home app
from home.views import index
from task.views import (main_dashboard, Dashboard_Categories_Month, 
                Dashboard_Status_Month, Dashboard_Tasks_Week, Dashboard_Goals_Quarter, 
                Dashboard_Long_Medium_Term_Goals, Dashboard_Goals_Status_Task)

#from user_profile.views import profile
from accounts import views as user_views

'''You can import the login/logout functionalities as template views in this file or you can customize them but you will have 
    to import them in your views.py file. '''
from django.contrib.auth import views as auth_views # we won't be using this because we have customized our Users model

urlpatterns = [
    path('', index, name='index'),
    path('admin/', admin.site.urls),
    path('register/', user_views.register_view, name='register'),
    #path('profile/', profile, name='profile'),
    #path('login/', user_views.login_view, name='login'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='accounts/logout.html'), name='logout'), # template view for logout
    
    # password reset
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='accounts/password_reset.html'), name='password_reset'), 
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'), name='password_reset_done'), 
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'), name='password_reset_confirm'), 
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'), name='password_reset_complete'), 
    
    path('main/', main_dashboard, name='main_dashboard'), # when you reach dashboard, go directly to look for the urls from the Task application
    path('profile/', include('user_profile.urls')),
    path('tasks/', include('task.urls')),
    path('goals/', include('goal.urls')),
    path('categories/', include('category.urls')),
    url(r'^activate/(?P<activation_key>\w+)/$', user_views.activation_view, name='activate_account'),

    path('main/dashboard_categories_month', Dashboard_Categories_Month.as_view()), # load this view in the main page
    path('main/dashboard_status_month', Dashboard_Status_Month.as_view()),         # load this view in the main page
    path('main/dashboard_points_week', Dashboard_Tasks_Week.as_view()),
    path('main/dashboard_goals_quarter', Dashboard_Goals_Quarter.as_view()),
    path('main/dashboard_long_medium_term_goal', Dashboard_Long_Medium_Term_Goals.as_view()),
    path('main/dashboard_goals_status_task', Dashboard_Goals_Status_Task.as_view())
]
