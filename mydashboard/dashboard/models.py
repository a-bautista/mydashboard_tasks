# Python Libraries
from datetime import date

from django.db import models
from django.utils import timezone

# Create your models here.
class Task(models.Model):
    responsible  = models.TextField(null=True)
    task = models.TextField(null=True)
    initial_date = models.DateField(default=timezone.now())
    ending_date  = models.DateField(null=True)

