# Python Libraries
from datetime import date

# Django Libraries
from django.db import models
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Q, F

from django.contrib.auth import get_user_model # this belongs from the main Django configuration and it has been customized

from goal.models import Goal
#from category.models import Category

'''We will be using the customized User model from Django to store all our users which will be stored in a postgresql db.'''
#User = get_user_model()

#from django.conf import settings
#User = settings.AUTH_USER_MODEL

# Create your models here.
# When you clone this repo run the following to apply the migrations correctly:  the python3 manager.py migrate --run-syncdb
# to retrieve the objects in the shell you type from task.models import Task

class Task(models.Model):

    # ------------------------- Initial definitions -----------------------------
    PERSONAL_DEVELOPMENT = 'Personal Development'
    LEISURE = 'Leisure'
    HOME = 'Home'
    JOB = 'Job'
    HEALTH = 'Health'
    FAMILY = 'Family'
    STUDIES = 'Studies'

    ACTIVE = 'Active'
    CANCELLED = 'Cancelled'
    FINALIZED = 'Finalized'

    # -------------------------- Options in the dropdown menu ------------------------

    CATEGORIES = [(PERSONAL_DEVELOPMENT, PERSONAL_DEVELOPMENT), (LEISURE, LEISURE), (HOME, HOME),
                  (JOB, JOB), (HEALTH, HEALTH), (FAMILY, FAMILY), (STUDIES, STUDIES)]

    # ACTIVE will go to the current value of itself (Active) and use it for data storage
    # The second ACTIVE is the human readable name that goes in the dropdown menu
    STATUS = [(ACTIVE, ACTIVE), (CANCELLED, CANCELLED), (FINALIZED, FINALIZED)]

    # ------------------------- Main fields --------------------------------------
    id           = models.AutoField(primary_key=True)
    #username     = models.ManyToManyField(User)
    #username     = models.ForeignKey(User, on_delete=models.CASCADE) # the name changes to username_id inside of the db automatically
    goal         = models.ManyToManyField(Goal)
    task         = models.CharField(null=False, max_length=140)
    #category     = models.ManyToManyField(Category)
    category     = models.CharField(max_length=24, choices=CATEGORIES, default=PERSONAL_DEVELOPMENT)
    status       = models.CharField(max_length=24, choices=STATUS, default=ACTIVE)
    points       = models.FloatField(default=5)
    life_task    = models.IntegerField(default=3) # task has a life of 4 weeks (3,2,1,0) to be completed

    initial_week = models.CharField(max_length=2, null=False, default=date.today().isocalendar()[1])
    initial_date = models.DateField(default=timezone.now(), null=False)
    ending_date  = models.DateField(default=timezone.now(), null=True)

    class Meta:
        ordering = ['initial_date']
        db_table = 'task_table'

    # ------------------------- Post Save --------------------------------------


def update_points(sender, instance, created, **kwargs):
    '''Every time a task is inserted, add 5 points to the previous task except the first one.'''
    INCREASE_POINT = 5

    if created:
        Task.objects.filter(~Q(pk=instance.pk), status='Active').update(points=F('points')+INCREASE_POINT)

    # Get only the tasks that are active, then order them by id in descending order and show all of them except the first one
    # qs = Task.objects.filter(status='Active').order_by('-id')[1:]

    # Another approach to do the same from above but that will involve changing the DateField to DateTimeField
    # qs = Task.objects.filter(status='Active').exclude(initial_date=Task.objects.all().aggregate(Max('initial_date'))['initial_date__max'])


post_save.connect(update_points, sender=Task)


