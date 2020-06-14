from django.db import models

from django.conf import settings
User = settings.AUTH_USER_MODEL

class Category(models.Model):

    # ------------------------- Main fields --------------------------------------
    id           = models.AutoField(primary_key=True)
    category     = models.CharField(max_length=60)
    description  = models.CharField(null=False, max_length=60)
    accounts     = models.ManyToManyField(User)
    

    class Meta:
        ordering = ['id']
        db_table = 'category_table'