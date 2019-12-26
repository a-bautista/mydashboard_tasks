# Python Libraries
from django.db import models
from django.utils import timezone
from django.db.models import Q, F
from django.db.models.signals import post_save

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
    STATUS = [(ACTIVE, ACTIVE), (CANCELLED, CANCELLED),
              (FINALIZED, FINALIZED)]

    # ------------------------- Main fields --------------------------------------
    id = models.AutoField(primary_key=True)
    responsible = models.CharField(
        null=False, max_length=120, default='Alejandro Bautista')
    task = models.CharField(
        null=False, max_length=140)


    category = models.CharField(
        max_length=24, choices=CATEGORIES, default=PERSONAL_DEVELOPMENT)
    status = models.CharField(max_length=24, choices=STATUS, default=ACTIVE)
    points = models.IntegerField(default=5)

    initial_week = models.CharField(max_length=2, null=False, default=date.today().isocalendar()[1])
    initial_date = models.DateField(default=timezone.now(), null=False)
    ending_date = models.DateField(null=True)

# ------------------------- Post Save --------------------------------------

    #@receiver(post_save, sender=Task)
    #def update_points(sender, instance, created, **kwargs ):
    #    if created:
    #       print("Object created")

def update_points(sender, instance, created, **kwargs):
    # Current value of increase points
    INCREASE_POINT = 5

    if created:
        Task.objects.filter(~Q(pk=instance.pk), status='Active').update(points=F('points')+5)

    # Get only the tasks that are active, then order them by id in descending order and show all of them except the first one
    #qs = Task.objects.filter(status='Active').order_by('-id')[1:]

    # Another approach to do the same from above but that will involve changing the DateField to DateTimeField
    # qs = Task.objects.filter(status='Active').exclude(initial_date=Task.objects.all().aggregate(Max('initial_date'))['initial_date__max'])

    # Increase the points of all the previous active tasks by 5
    #for task in qs:
    #    task.points = task.points + INCREASE_POINT
        #task.save()

post_save.connect(update_points, sender=Task)