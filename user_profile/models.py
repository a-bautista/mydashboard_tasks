from django.db import models

from django.conf import settings
User = settings.AUTH_USER_MODEL

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    #timestamp = models.DateTimeField

    class Meta:
        #ordering = ['']
        db_table = 'profile_table' # this is the name that will be used for the table goal

    def __str__(self):
        return f'{self.user.username} Profile'

