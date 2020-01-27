# Python Libraries
from datetime import date

# Django Libraries
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class MyAccountManager(BaseUserManager):
     
     def create_user(self, email, username, first_name, last_name, score, password=None):
        
          if not email:
               raise ValueError("User must have an email address.")
          if not username:
               raise ValueError("User must have a username.")
          if not first_name:
               raise ValueError("User must have a first name.")
          if not last_name:
               raise ValueError("User must have a last name.")
          

          user = self.model(email=self.normalize_email(email),
                 username=username,
                 first_name = first_name,
                 last_name = last_name,
                 score = score,
          )

          user.set_password(password)
          user.save(using=self._db)
          return user

     def create_superuser(self, email, username, first_name, last_name, score, password):
          
          user = self.create_user(email=self.normalize_email(email),
               username=username,
               first_name = first_name,
               last_name = last_name,
               score = score,
               password=password, 
          )

          user.is_admin = True
          user.is_staff = True
          user.is_superuser = True
          user.save(using=self._db)
          return user


class Account(AbstractBaseUser):
     email        = models.EmailField(verbose_name="email", max_length=60, unique=True)
     username     = models.CharField(max_length=30, unique=True)
     first_name   = models.CharField(max_length=25)
     last_name    = models.CharField(max_length=25)
     score        = models.FloatField(default=100)
     #image        = models.ImageField(default='default.jpg', upload_to='profile_pics')

     # The following fields are required for every customer User model
     last_login   = models.DateTimeField(verbose_name='last login', auto_now=True)
     date_joined  = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
     is_admin     = models.BooleanField(default=False)
     is_active    = models.BooleanField(default=True)
     is_staff     = models.BooleanField(default=False)
     is_superuser = models.BooleanField(default=False)

     USERNAME_FIELD = 'email' 
     REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'score']

     objects = MyAccountManager()

     def __str__(self):
          return self.email
     
     def has_perm(self, perm, obj=None):
          return self.is_admin
     
     def has_module_perms(self, app_label):
          return True

# Create your models here.
# When you clone this repo run the following to apply the migrations correctly:  the python3 manager.py migrate --run-syncdb
# to retrieve the objects in the shell you type from task.models import Task
