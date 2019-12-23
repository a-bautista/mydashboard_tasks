# Python Libraries
from django.db import models
from django.utils import timezone
from datetime import date
#from django.utils.translation import gettext_lazy as _

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
    id = models.AutoField(primary_key=True)
    responsible = models.CharField(
        null=False, max_length=120, default='Alejandro Bautista')
    task = models.CharField(
        null=False, max_length=140)

    category = models.CharField(
        max_length=24, choices=CATEGORIES, default=PERSONAL_DEVELOPMENT)
    status = models.CharField(max_length=24, choices=STATUS, default=ACTIVE)

    initial_week = models.CharField(max_length=2, null=False, default=date.today().isocalendar()[1])
    initial_date = models.DateField(default=timezone.now(), null=False)
    ending_date = models.DateField(null=True)
