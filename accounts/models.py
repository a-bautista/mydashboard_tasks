# Python Libraries
from datetime import date

# Django Libraries
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class MyAccountManager(BaseUserManager):
     
     def create_user(self, email, username, password=None):
        
          if not email:
               raise ValueError("User must have an email address.")
          if not username:
               raise ValueError("User must have a username.")
          

          user = self.model(email=self.normalize_email(email),
                 username=username,
                 
          )

          user.set_password(password)
          user.save(using=self._db)
          return user

     def create_superuser(self, email, username, password):
          
          user = self.create_user(email=self.normalize_email(email),
               username=username,
               password=password, 
          )

          user.is_admin = True
          user.is_staff = True
          user.is_superuser = True
          user.save(using=self._db)
          return user


class Account(AbstractBaseUser):
     id           = models.AutoField(primary_key=True)
     email        = models.EmailField(verbose_name="email", max_length=60, unique=True)
     username     = models.CharField(max_length=30, unique=True)
     
     # The following fields are required for every customer User model
     last_login   = models.DateTimeField(verbose_name='last login', auto_now=True)
     date_joined  = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
     is_admin     = models.BooleanField(default=False)
     is_active    = models.BooleanField(default=True)
     is_staff     = models.BooleanField(default=False)
     is_superuser = models.BooleanField(default=False)

     USERNAME_FIELD = 'username' # this field is used for the login
     REQUIRED_FIELDS = ['email'] # the username field should not be included in the required field

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

class EmailConfirmed(models.Model):
     # django created automatically the id column
     username         = models.OneToOneField(Account, on_delete = models.CASCADE)
     activation_key   = models.CharField(max_length=200)
     key_expires      = models.DateTimeField()
     user_confirmed   = models.BooleanField(default=False)

     class Meta:
         ordering = ['activation_key']
         db_table = 'accounts_emailconfirmed'