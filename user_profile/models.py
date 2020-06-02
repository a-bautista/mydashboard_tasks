from django.db import models

from django.conf import settings
User = settings.AUTH_USER_MODEL

class Profile(models.Model):
    user                = models.OneToOneField(User, on_delete = models.CASCADE)
    first_name          = models.CharField(max_length=40, blank=True)
    last_name           = models.CharField(max_length=60, blank=True)
    image               = models.ImageField(default='default.png', upload_to='profile_pics')
    score               = models.FloatField(default=100)
    task_increase_point = models.IntegerField(default=5)
    max_task_life_week  = models.IntegerField(default=4)



    class Meta:
        #ordering = ['']
        db_table = 'profile_table' # this is the name that will be used for the table goal
        #exclude = ['user'] # users won't be able to modify the name of their usernames

    def __str__(self):
        return f'{self.user.username} Profile'