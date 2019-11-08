# Python Libraries
from django.db import models
from django.utils import timezone

# Create your models here.
# When you clone this repo run the following to apply the migrations correctly:  the python3 manager.py migrate --run-syncdb
# to retrieve the objects in the shell you type from task.models import Task
class Task(models.Model):
    CATEGORIES = (('DV', 'Dataviews'), ('SOX', 'SOX-Compliance issues'), ('TRS', 'Troubleshooting'),
                  ('PSQL', 'Programming SQL'), ('AUT', 'Automation'), ('SL', 'SyteLine troubleshooting'))
    STATUS = (('A', 'Active'), ('C', 'Cancelled'), ('D', 'Done'))

    responsible  = models.CharField(null=False, max_length=120, default='Alejandro Bautista')
    task = models.TextField(null=False, default='Start typing your task here ...')

    category = models.CharField(max_length=24, choices=CATEGORIES, default='SyteLine troubleshooting')
    status = models.CharField(max_length=24, choices=STATUS, default='A')

    initial_date = models.DateField(default=timezone.now(), null=False)
    ending_date  = models.DateField(null=True)
