Author: Alejandro Bautista Ramos
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

There is NO need to type in the credentials of your db in the django app because heroku manages this automatically (this applies for creating an app with a container and via Git).

### Debugging your tables:

Below you will find the main tables that you need to work on.
`select * from pg_catalog.pg_tables where tableowner <> 'postgres';`


# Creating the tables manually (not necessary because when you make the migrations and then apply the changes, they will be reflected automatically)

## create the table task based on the models.py file (notice the name must be task_task to make this working):

`create table task_task(id serial, responsible text, task text, category text, status text, initial_date date, ending_date date);`

## table for the user points
`CREATE TABLE TASK_USER_POINTS(id serial, points text);`

## table for the customized User model

`CREATE TABLE ACCOUNTS_ACCOUNT(EMAIL TEXT, USERNAME TEXT, FIRST_NAME TEXT, LAST_NAME TEXT, SCORE FLOAT, PASSWORD varchar, LAST_LOGIN TIMESTAMP, DATE_JOINED TIMESTAMP, IS_ADMIN BOOLEAN, IS_ACTIVE BOOLEAN, IS_STAFF BOOLEAN, IS_SUPERUSER BOOLEAN, ID SERIAL);`

## alter the table task_task for changing the responsible to username

`ALTER TABLE TASK_TASK`
`RENAME COLUMN responsible TO username_id;`

After you have created the db, you need to apply the migrations and create a super user:

    `heroku run python3 manage.py migrate -a djangodocker`
    `heroku run python3 manage.py makemigrations -a djangodocker`
    `heroku run python3 manage.py createsuperuser -a djangodocker`


### Heroku with containerized docker

## set the volumes

    sudo docker run -p 3000:8888 -v$(pwd):/app  mydashboard_web


### 1. Type the following command to apply the `sudo heroku container:login` successfully. This command provides the login to connect into the Heroku Container Registry.

    `sudo apt install gnupg2 pass`


### 2. Create a new project and login into the Heroku Container Registry

    `heroku login`

    `heroku create telos-dashboard`

    `sudo heroku container:login`

### 2.5 In case you want to download the docker image to your machine

    `sudo heroku container:pull web -a telos-dashboard-container`

### 3. Provide the PostgreSQL database for production

    `heroku addons:create heroku-postgresql:hobby-dev -a djangodocker`

### 4. Install the postgresql dependency

    `pipenv install dj-database-url psycopg2`

### 5. Update the Django Database Settings in the `settings.py`

        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
            }
        }

        # Heroku settings that need to be added
        `import dj_database_url`
        `db_from_env = dj_database_url.config()`
        `DATABASES['default'].update(db_from_env)`
        `DATABASES['default']['CONN_MAX_AGE'] = 500`

### 6. Modify the `settings.py` to include the following line for rendering templates.

    `TEMPLATES = [ ....`
        `'DIRS': [os.path.join(BASE_DIR, 'templates')],`
     `..]`

### 7. Install the pipenv dependencies with the command pipenv install

### 8. Run the following command at the same level of your manage.py file (you must have your virtual environment activated to run this command with the gunicorn library installed):

    `gunicorn djangodocker.wsgi:application --bind 0.0.0.0:8888`

## 9. There should be 2 Dockerfiles, one for heroku and the other one for local testing.

    `Dockerfile.dev` - sudo docker build -t abautista/django-docker -f Dockerfile.dev .

    `Dockerfile` - sudo docker build -t abautista/django-docker-heroku -f Dockerfile .

For testing you image locally, you need to execute the command `sudo docker run -p 3000:8888 <image_id>`.

### 11. Create the docker image that will be released in Heroku. Run the command at the same level of the Dockerfile.

    `sudo docker build -t abautista/django-docker-heroku .`

### 12. Push the image into Heroku (djangodocker is the name of your app)

    `sudo heroku container:push web -a djangodocker`
    `sudo heroku container:push web -a telos-dashboard-container`

### 13. Release the image in heroku

    `sudo heroku container:release web -a djangodocker`
    `sudo heroku container:release web -a telos-dashboard-container`

### 14. Open the heroku app to verify that it is working.

    `heroku open -a djangodocker`

### 15. Make the migrations in the Docker container after you have changed the configuration.
    
    `heroku run python3 manage.py makemigrations -a telos-dashboard-container`
    `heroku run python3 manage.py migrate -a telos-dashboard-container`

    In case you cannot do it with the command from above use the following:

    `heroku run bash -a telos-dashboard-container`
    `cd src`
    `python3 manage.py makemigrations`
    `python3 manage.py migrate`


### 16. Creating a super user to manage.

    `heroku run python3 manage.py createsuperuser -a telos-dashboard-container`

### Additional notes

#### See the logs in Heroku in case something has failed.

    `heroku logs -a djangodocker --tail`

#### Log into the bash of the Heroku app.

    `heroku run bash -a djangodocker`
    `heroku run bash -a telos-dashboard-container`

#### Map your container 
`heroku run python3 manage.py runserver -a telos-dashboard-container && heroku run -p 3000:8888`


#### Pass a command through the docker container

`sudo docker exec -it mydashboard_web_1 sh`
`sudo docker exec -it mydashboard_web_1 python manage.py makemigrations`
`sudo docker exec -it mydashboard_web_1 python manage.py migrate goal`
`sudo docker exec -it mydashboard_web_1 python manage.py migrate account`

#### Testing with AWS

In order to run your app with AWS, we need to create each service (Django, Nginx and PostgreSQL) separately. For doing that we need to create the docker-compose.yml file
and modify the settings.py to add the following lines:

`settings.py`
`DATABASES = {`
    `'default': {`
        `'ENGINE': 'django.db.backends.postgresql',`
        `'NAME': 'postgres',`
        `'USER': 'postgres',`
        `'HOST': 'db',`
        `'PORT': 5432`
        `#If there is not any password set up then everyone can access to this db`
    `}
`}`

`docker-compose.yml`

`version: "3"`

`services:``
  `web: # this is the name of your first container`
    `build: . # this is equivalent to sudo docker build . (executes the Dockerfile)`
    `ports:`
      `- "3000:8888" # map from your web browser port 3000 to container port 8888`

    `depends_on: # this indicates to run the db before the web service`
    `  - db`

  `db: # this is the name of your second container`
    `image: postgres:11`

The ports that were setup in the web service are used to map your container to your web browser, so your port `localhost:3000` will redirect you to the port 8888
of your container.

The postgres container is created from the docker-compose.yml file and once it is running you can connect to the database  with:

`sudo docker exec -it mydashboard_db_1 psql -U postgres` and then create your table task:

You can see all your running container from the docker-compose with the command `docker-compose ps` and you can delete all those container with `docker-compose rm`.

Then you insert the following command to create your table.

`create table task_task(id serial, responsible text, task text, category text, status text, initial_date date, ending_date date);`

Every time you access to the container, the database will be already there but in case you encounter problems within it, you should destroy all the images with
`sudo docker-compose rm`.

After creating the database, you should be able to use all the CRUD operations.

If for some reason you need to change a database column and you are already using docker-compose and you encounter this error
`psql: could not translate host name "postgres" to address: Temporary failure in name resolution` then you can bypass it with the following command:

`sudo docker exec -it mydashboard_db_1 psql -h 127.0.0.1 -p 5432 -U postgres` where mydashboard_db_1 is the name of you db container, -h 127.0.0.1 indicates
to connect from the host and -p to use the port 5432 that belongs to the container.

For altering a table to add a new column you use:

`alter table task_task add column initial_week smallint;`

### Working with nginx

What nginx does is that instead of using Django as the server for displaying your app, it  will be using nginx. You need to create a separate folder with its Dockerfile
and the nginx.conf file. nginx is a server that can handle routing between server and client and other different services but for this app we won't touch into details
about all these services.

You can use `docker-compose up` to start running all your containers.

### Deploying to .travis -> DockerHub -> AWS Elastic Bean Stalk

The .travis file has the purpose to create the images of your containers, perform tests and push them to DockerHub, so AWS can use them to deploy your app.

You need to create the Dockerrun.aws.json file to configure the containers that you want to run because for AWS, that's the equivalent to docker-compose.yml file.
When you deploy an app through Amazon Elastic Bean Stalk, this one uses the Amazon Elastic Container Service (ECS) for running containers. The ECS have task definitions
which contain instructions about how to run a single container.

In AWS you have to create your Elastic Bean Stalk service to deploy your application but you need to create separate services such as the RDB configure the security groups,
so you can connect your database container with the Amazon RDB service. When creating the EBS, you need to select the platform as multi container docker and then you click on the
create environment.
In your Amazon account there is something called the Default Virtual Private Cloud (VPC) which is used to contain all the services that you create. By default,
all the services you create are disconnected and the VPC is used to bundle them together so they can start talking to each other. VPC are assigned as default per region.
When you type VPC and then on Your VPCs you will find your default VPC. In order to connect your different services through the VPC, you need to configure the security
group which are the rules that describe which services can connect through the VPC (you can find the security groups created under the VPC service and then look for security groups).

To create an RDS service you type RDS and then you select the postgresql service, then you click on next and you set the following points:

DB instance id: telos-db
DB name or initial db name: postgres
PORT: 5432
engine version : 11.1 (because that's almost the same version of your container)
disable the automatic backups
master username: postgres
password: (use the same as you defined in your settings file)

In network and security, you select the Default VPC, in public accessibility you select NO, then you select the create VPC security group.
Now you need to create the custom security group, then you click on VPC and then you look for Security groups and then you hit on the Create Security
Group and you put the name such as the name of your app, then you select your default VPC. Then you click on the Inboud rules and then you click on
Edit and you leave Custom TCP, then you put the ports range 5432 which belongs to postgres and for the source you selec the Group ID of your newly
created security group.

Now you you go back to the postgresql to add the security group. You select RDS, then you click on Instances and click on Modify then you go to Network and security and you add the security group
you created previously. You click on apply immediately and then you click on Modify DB instance. You go back to the EBS and then you click on configuration and you select EC2 to select the security
group you want to add in your EBS application.

You go back to your elastic beanstalk, then you click on configuration and select your newly created security group in the EC2 menu.

You set up the environment rules by going to configuration and under the software section you click on modify and you put all your postgresql variables that you defined on your docker-compose.yml file.
When you type the PGHOST you need to look for the instance of your RDS full value (us-west-2.rds.amazonaws.com)

Then you need to configure the IAM (User Access and Encryption keys) by selecting IAM from the main menu and then you create your new user, then you set your permissions by selecting
attach existing policies directly and then on the search menu you type  beanstalk and you select all your permissions for now. You copy the access variables that are provided and you paste them
in your travis-ci account under settings and then you create the protected variables for storing the keys.


#### Adding a domain with Heroku and GoDaddy


You need to apply the following command `heroku domains:add www.telos-app.xyz -a telos-dashboard-container`

add a wildcard for your app `heroku domains:add *.telos-app.xyz -a telos-dashboard-container`

In Godaddy, look for the DNS management and add the CNAME www and * and insert the values that you have from the settings
in your Heroku configuration.

Activate the forwarding domain and put the name of your app. 


#### In case your encounter the error:
 `unauthorized: authentication required`
 `▸    Error: docker push exited with Error: 1`

`sudo heroku container:login`


#### How does the hashing works in the email?


#### generate the hash for the activation url
            `short_hash = hashlib.sha256(str(os.urandom(256)).encode('utf-8')).hexdigest()[:10]`
            `activation_key = hashlib.sha256(str(short_hash+context['username']).encode('utf-8')).hexdigest()`
            `context['activation_key'] = activation_key`
            `UserRegisterForm.activate_user_email(UserRegisterForm,context)`


##### Details of data types in postgresql

`\d+ task_table_goal;`


##### Serving files with S3 Amazon bucket for production

You need to create a S3 bucket, create an IAM user and provide the credentials in heroku for storing files.
Then you need to install 2 packages: boto3 and django-storages.
When you create your S3 bucket you need to configure the CORS file with the following:

<?xml version="1.0" encoding="UTF-8"?>
<CORSConfiguration xmlns="http://s3.amazonaws.com/doc/2006-03-01/">
   <CORSRule>
        <AllowedOrigin>*</AllowedOrigin>
        <AllowedMethod>GET</AllowedMethod>
        <AllowedMethod>POST</AllowedMethod>
        <AllowedMethod>PUT</AllowedMethod>
        <AllowedHeader>*</AllowedHeader>
    </CORSRule>
</CORSConfiguration>

Add the following lines to the settings.py file and include the `storages` app in installed_apps.

# AWS storage keys
AWS_ACCESS_KEY_ID       = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY   = os.environ['AWS_SECRET_ACCESS_KEY']
AWS_STORAGE_BUCKET_NAME = os.environ['AWS_STORAGE_BUCKET_NAME']

# files won't be overwritten but renamed
AWS_S3_FILE_OVERWRITE = False

# set this to None due to functionality
AWS_DEFAULT_ACL = None

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# Debug your heroku container

Get access to your container with:

    `heroku run bash -a telos-dashboard-container`

Get access to the Django queries with:

    `python manage.py shell`

Some queries that I had to execute to troubleshoot a problem were:

    `qs_tasks = Task.objects.filter(status='Active')`

    `>>> from task.models import Task`
    `>>> from goal.models import Goal`
    `>>> qs_current_user_goals = Goal.objects.filter(accounts='3', status='In Progress').values('id').values_list('id')`
    >>> qs_current_user_goals
    `<QuerySet [(13,), (12,), (22,), (29,), (30,), (34,), (35,), (33,), (37,)]>`

    `qs_current_user_goals = Goal.objects.filter(accounts='3', status='In Progress')`
    `>>> qs_current_user_goals`
    `<QuerySet [<Goal: Goal object (13)>, <Goal: Goal object (12)>, <Goal: Goal object (22)>, <Goal: Goal object (29)>, <Goal: Goal object (30)>, <Goal: Goal object (34)>, <Goal: Goal object (35)>, <Goal: Goal object (33)>, <Goal: Goal object (37)>]>  
    `>>> for goal in qs_current_user_goals:`
         `print(goal.goal)`