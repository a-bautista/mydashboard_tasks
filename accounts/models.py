# Python Libraries
from datetime import date

# Django Libraries
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
#from django.apps import apps
from goal.models import Goal, UserToGoal

#import django, os
#os.environ.setdefault()

# Import the model from the app goal
#Goal = apps.get_model('goal', 'Goal') # app_name and model_name
#Task = apps.get_model('task', 'Task')

# Additional notes
# django.db.utils.ProgrammingError: there is no unique constraint matching given keys for referenced table "accounts_account"
# the solution was to create a Fk as `alter table accounts_account add constraint accounts_account_fk unique (id);`

class MyAccountManager(BaseUserManager):
     
     def create_user(self, email, username, score, password=None):
        
          if not email:
               raise ValueError("User must have an email address.")
          if not username:
               raise ValueError("User must have a username.")
          # I deactivated the first_name and last_name fields, so you can register only with your email and password
          #if not first_name:
          #     raise ValueError("User must have a first name.")
          #if not last_name:
          #     raise ValueError("User must have a last name.")
          

          user = self.model(email=self.normalize_email(email),
                 username=username,
                 # these records won't be written to the db
                 #first_name = first_name,
                 #last_name = last_name,
                 score = score,
          )

          user.set_password(password)
          user.save(using=self._db)
          return user

     def create_superuser(self, email, username, score, password):
          
          user = self.create_user(email=self.normalize_email(email),
               username=username,
               score = score,
               password=password, 
          )

          user.is_admin = True
          user.is_staff = True
          user.is_superuser = True
          user.save(using=self._db)
          return user


class Account(AbstractBaseUser):
     '''
          This is how you declare an account in the shell.
          user1 = Account.objects.create(email='a2@hotmail.com', username='a2', score='100')
     '''
     id           = models.AutoField(primary_key=True)
     email        = models.EmailField(verbose_name="email", max_length=60, unique=True)
     username     = models.CharField(max_length=30, unique=True)
     #first_name   = models.CharField(max_length=25) # not mandatory in the db
     #last_name    = models.CharField(max_length=25) # not mandatory in the db
     score        = models.FloatField(default=100)
     #image        = models.ImageField(default='default.jpg', upload_to='profile_pics')
     goal         = models.ManyToManyField(Goal, through=UserToGoal)
     #task         = models.ManyToManyField('Task', blank=True, null=True)


     # The following fields are required for every customer User model
     last_login   = models.DateTimeField(verbose_name='last login', auto_now=True)
     date_joined  = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
     is_admin     = models.BooleanField(default=False)
     is_active    = models.BooleanField(default=True)
     is_staff     = models.BooleanField(default=False)
     is_superuser = models.BooleanField(default=False)

     USERNAME_FIELD = 'email' 
     # first_name and last_name can be commented in the REQUIRED_FIELDS
     REQUIRED_FIELDS = ['username'
                       #,'first_name'
                       #, 'last_name'
                       , 'score']

     objects = MyAccountManager()

     def __str__(self):
          '''Returns the email whenever you type an instance of an account.'''
          return self.email
     
     def has_perm(self, perm, obj=None):
          return self.is_admin
     
     def has_module_perms(self, app_label):
          return True

# Create your models here.
# When you clone this repo run the following to apply the migrations correctly:  the python3 manager.py migrate --run-syncdb
# to retrieve the objects in the shell you type from task.models import Task
