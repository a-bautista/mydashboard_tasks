# Python Libraries
from django.db import models
from django.utils import timezone

# Create your models here.
# When you clone this repo run the following to apply the migrations correctly:  the python3 manager.py migrate --run-syncdb
# to retrieve the objects in the shell you type from task.models import Task
class Task(models.Model):
    responsible  = models.CharField(null=False, max_length=120, default='Alejandro Bautista')
    task = models.TextField(null=True)
    initial_date = models.DateField(default=timezone.now(), null=False)
    ending_date  = models.DateField(null=True)

