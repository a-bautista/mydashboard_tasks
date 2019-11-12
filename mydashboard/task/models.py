# Python Libraries
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

# Create your models here.
# When you clone this repo run the following to apply the migrations correctly:  the python3 manager.py migrate --run-syncdb
# to retrieve the objects in the shell you type from task.models import Task


class Task(models.Model):

    DATAVIEWS = 'Dataviews'
    SOX_COMPLIANCE_ISSUES = 'SOX Compliance Issues'
    TROUBLESHOOTING = 'Troubleshooting'
    PROGRAMMING_SQL = 'Programming SQL'
    AUTOMATION = 'Automation'
    SYTELINE_TROUBLESHOOTING = 'SyteLine Troubleshooting'

    ACTIVE = 'Active'
    CANCELLED = 'Cancelled'
    FINALIZED = 'Finalized'

    CATEGORIES = [(DATAVIEWS, DATAVIEWS), (SOX_COMPLIANCE_ISSUES, SOX_COMPLIANCE_ISSUES), (TROUBLESHOOTING, TROUBLESHOOTING),
                  (PROGRAMMING_SQL, PROGRAMMING_SQL), (AUTOMATION, AUTOMATION), (SYTELINE_TROUBLESHOOTING, SYTELINE_TROUBLESHOOTING)]

    # ACTIVE will go to the current value of itself (Active) and use it for data storage
    # The second ACTIVE is the human readable name that goes in the dropdown menu
    STATUS = [(ACTIVE, ACTIVE), (CANCELLED, CANCELLED),
              (FINALIZED, FINALIZED)]

    responsible = models.CharField(
        null=False, max_length=120, default='Alejandro Bautista')
    task = models.TextField(
        null=False, default='Start typing your task here ...')

    category = models.CharField(
        max_length=24, choices=CATEGORIES, default=SYTELINE_TROUBLESHOOTING)
    status = models.CharField(max_length=24, choices=STATUS, default=ACTIVE)

    initial_date = models.DateField(default=timezone.now(), null=False)
    ending_date = models.DateField(null=True)
