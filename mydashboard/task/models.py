# Python Libraries
from django.db import models
from django.utils import timezone

# Create your models here.
class Task(models.Model):
    responsible  = models.CharField(null=False, max_length=120, default='Alejandro Bautista')
    task = models.TextField(null=True)
    initial_date = models.DateField(default=timezone.now(), null=False)
    ending_date  = models.DateField(null=True)

