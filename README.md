## Installing PostgreSQL

### 1. Installing PostgreSQL in Windows

Go to the following website to install PostgreSQL: https://www.enterprisedb.com/downloads/postgres-postgresql-downloads

### 2. Installing PostgreSQL in Linux (For dev purposes, not for live)

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
    `\du` -- check all the current users
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


### Testing with Heroku (Dev)

Install gunicorn

    `pip3 install gunicorn`

Create the file Procfile with the contents (install gunicorn first):

    `web: gunicorn <name_of_your_app>.wsgi --log-file -`

Create a runtime.txt file which will contain the version of your Python version:

    `python-3.6.9`

Install whitenoise for the production file

    `pip3 install whitenoise`

In order to fix the static media files you need to add the following line in the middleware section from the local.py file.

'whitenoise.middleware.WhiteNoiseMiddleware', # this line is mandatory in order to see the css and images

Make sure to have the correct path for displaying the media files:

`BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))`

Allow the following hosts:

`ALLOWED_HOSTS = ['0.0.0.0', 'localhost:5000', '127.0.0.1', 'localhost']`

View the changes with `heroku local web`

### Testing with Heroku (Live)

Create the name of you heroku app:

    `heroku create dashboard-telos`

Create the Heroku repo and add it to your list of remotes:

    `git remote add heroku https://git.heroku.com/dashboard-telos.git`

    In case you need to remove the repo you use:

    `git remote remove heroku`

Install gunicorn

    `pip3 install gunicorn`

Create the file Procfile with the contents (install gunicorn first):

    `web: gunicorn <name_of_your_app>.wsgi --log-file -`

Create a runtime.txt file which will contain the version of your Python version:

    `python-3.6.9`

Install whitenoise for the production file

    `pip3 install whitenoise`

Create your secret keys for the settings file:

    `heroku config:set SECRET_KEY="<settings_password>"`

Use the free version of postgresql that is included:

    `heroku addons:create heroku-postgresql:hobby-dev`

In order to fix the static media files you need to add the following line in the middleware section from the local.py file.

'whitenoise.middleware.WhiteNoiseMiddleware', # this line is mandatory in order to see the css and images

Make sure to have the correct path for displaying the media files:

`BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))`

Allow the following hosts:

`ALLOWED_HOSTS = ['dashboard-telos.herokuapp.com']`

Add the files you have modified, then commit the changes and push them to Heroku:

`git add -A`
`git push heroku master`

### Connect to the postgresql database and create the initial tables

Go to data.heroku.com, then select your db and click on the settings option and click on the view credentials button to see the configuration that you need
to connect to your database. In order to connect to the db, you should type a command similar to the following:

`heroku pg:psql postgresql-transparent-84888 --app dashboard-telos`
  or
`heroku pg:psql --app dashboard-telos`

create the table task based on the models.py file (notice the name must be task_task to make this working):

`create table task_task(id serial, responsible text, task text, category text, status text, initial_date date, ending_date date);`

