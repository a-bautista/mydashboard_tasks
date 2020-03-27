# Create your models here.
# Django libraries

from django.db import models
#from django.apps import apps
from django.utils import timezone
#from django.contrib.auth.models import AbstractBaseUser
#from django.contrib.auth import get_user_model

#User = get_user_model()

# the line from below is the only way to import the User model and use it as a Fk
from django.conf import settings
User = settings.AUTH_USER_MODEL

#from task.models import Task # why this one doesn't work?


#from goal.models import Goal

'''Declare the class to indicate the data that will be stored. '''
#Task = apps.get_model('task', 'Task') # app_name and model_name
#User = apps.get_model('accounts', 'Account')


class Goal(models.Model):

    # ------------------------- Initial definitions -----------------------------
    COMPLETED = 'Completed'
    NOT_COMPLETED = 'Not completed'
    CANCELLED = 'Cancelled'
    IN_PROGRESS = 'In Progress'

    LONG = 'Long'
    MEDIUM = 'Medium'
    SHORT = 'Short'

    # -------------------------- Options in the dropdown menu ---------------------
    STATUS = [(COMPLETED, COMPLETED), (NOT_COMPLETED, NOT_COMPLETED), (CANCELLED, CANCELLED), (IN_PROGRESS, IN_PROGRESS)]
    TYPE   = [(LONG, LONG), (MEDIUM, MEDIUM), (SHORT,SHORT)]

     # ------------------------- Main fields --------------------------------------
    id               = models.AutoField(primary_key=True)
    goal             = models.CharField(null=False, max_length=60)
    #user             = models.ForeignKey(User, on_delete = models.CASCADE) # this is the id of the user
    
    initial_date     = models.DateField(default=timezone.now(), null=False)
    expiration_date  = models.DateField()
    status           = models.CharField(max_length=24, choices=STATUS, default=IN_PROGRESS)
    goal_type        = models.CharField(max_length=10, choices=TYPE, default=SHORT)
    comments         = models.CharField(max_length=200)
    final_notes      = models.CharField(max_length=200)
    accounts         = models.ManyToManyField(User)
    #task             = models.ManyToManyField(Task)
    #registry         = models.ManyToManyField(GeneralRegistry, through_fields=id)
    
    class Meta:
        ordering = ['initial_date']
        db_table = 'goal_table' # this is the name that will be used for the table goal


#class UserToGoal(models.Model):
    '''
        This is how you can define a relationship to this table.
        Cannot assign "1": "UserToGoal.goal" must be a "Goal" instance.
        r1 = UserToGoal(user=user1, goal=goal, expiration_date = date(2020,3,31), status='IN_PROGRESS', comments= 'None', final_notes='None')
        
        Get all the details of the goal for user 8
        user1_detailed_goal = UserToGoal.objects.filter(user=8)
    '''

    # ------------------------- Initial definitions -----------------------------
    #COMPLETED = 'Completed'
    #NOT_COMPLETED = 'Not completed'
    #CANCELLED = 'Cancelled'
    #IN_PROGRESS = 'In Progress'

    # -------------------------- Options in the dropdown menu ---------------------
    #STATUS = [(COMPLETED, COMPLETED), (NOT_COMPLETED, NOT_COMPLETED), (CANCELLED, CANCELLED), (IN_PROGRESS, IN_PROGRESS)]

    #user             = models.ForeignKey(User, on_delete = models.CASCADE) # this is the id of the user
    #goal             = models.ForeignKey(Goal, on_delete = models.CASCADE) # this is the id of the goal
    #initial_date     = models.DateField(default=timezone.now(), null=False)
    #expiration_date  = models.DateField()
    #status           = models.CharField(max_length=24, choices=STATUS, default=IN_PROGRESS)
    #comments         = models.CharField(max_length=200)
    #final_notes      = models.CharField(max_length=200)


