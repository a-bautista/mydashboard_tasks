## Installing PostgreSQL

### 1. Installing PostgreSQL in Windows

Go to the following website to install PostgreSQL: https://www.enterprisedb.com/downloads/postgres-postgresql-downloads

### 2. Installing PostgreSQL in Linux

Use the following command to install PostgreSQL:

    `sudo apt update`
    `sudo apt install postgresql postgresql-contrib`

Once the installation has completed, you can log in PostgreSQL by typing:

    `sudo su - postgres`
    `psql`

In case you want to exit you type:

    `\q`


Other steps that you need to perform in the db:

    `\conninfo` -- check to which database and port your are currently connected
    `select version();` -- check the current version of postgres
    `select * from pg_database where datistemplate = false;` -- check all the databases
    `du\` -- check all the current users
    `alter role postgres with password 'new_password'` -- change the password of user postgres
    `create database mydashboard_tasks owner = postgres;` -- create the mydashboard_tasks db
    `psql mydashboard_tasks postgres`; -- connect to the newly created db
    `` -- create the table task

Aditional steps that you need to do in Django:

    `python manage.py createsuperuser` # create the super user
    `python manage.py makemigrations`  # make migrations
    `python manage.py migrate`         # apply migrations


### 2. Using Postgresql with Django

After installing Postgresq you need to create a new database by opening pgAdmin and then you create a new 
database by doing a right into Databases. 

After creating the database, you need to modify the `settings.py` file by changing the database configuration
to the following:

`DATABASES = 
    {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'mydashboard_tasks',
        'USER': 'postgres',
        'PASSWORD': '', 
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}`   

Then you need to apply the migrations with :
    
    `python manage.py makemigrations`
    `python manage.py migrate`
    
Then you need to create a super user with the following:

    `python manage.py createsuperuser`

In Postgres you can see all your tables by typing:  

`select * from pg_catalog.pg_tables;`



### References:

https://linux4one.com/how-to-install-postgresql-on-linux-mint-19/


## Submitting to Heroku


### Testing with Heroku local web

Create the name of you heroku app:

    `heroku create dashboard-telos`

Create the Heroku repo and add it to your list of remotes:

    `git remote add heroku https://git.heroku.com/dashboard-telos.git`

    In case you need to remove the repo you use:

    `git remote remove heroku`

Create the file Procfile with the contents (install gunicorn first):

    `pip3 install gunicorn`
    `web: gunicorn <name_of_your_app>.wsgi --log-file -`

Create a runtime.txt file which will contain the version of your Python version:

    `python-3.6.7`

Create your secret keys for the settings file:

    `heroku config:set SECRET_KEY="<settings_password>"`

 Install whitenoise for the production file

    `pip3 install whitenoise`

 This project has the following structure:

 mydashboard_tasks
    |----mydashboard
            | components
            | live-static
            | static
            | task
            | templates
            | db.sqlite3
            | manage.py
            | mydashboard ----------| __init__.py
            |                       | settings.py
            |                       | urls.py
            |                       | wsgi.py
            |                       | forms.py
            | .gitignore
            | Dockerfile
            | Dockerfile-local
            | Procfile
            | README.md
            | requirements.txt
            | runtime.txt
            | ToDo.txt

 Because of the following file structure of the app, the wsgi.py, Procfile, Local and Production files, and mydashboard/url.py files
 need to be modified to include the new route of the file structure, i.e.,mydashboard.mydashboard.settings, mydashboard.mydashboard.wsgi,
 mydashboard.mydashboard.wsgi.application, mydashboard.task (from the installed_apps), mydashboard.task.urls.

After this you can try running heroku with `heroku local web`.

In order to fix the static media files you need to add the following line in the middleware section from the local.py file.

'whitenoise.middleware.WhiteNoiseMiddleware', # this line is mandatory in order to see the css and images