from django.db import models
#from task.models import Task
# Create your models here.

class Category(models.Model):

    id       = models.AutoField(primary_key=True)
    category = models.CharField(null=False, max_length=40)
    comments = models.CharField(max_length=200)

    class Meta:
        db_table = 'category_table' 