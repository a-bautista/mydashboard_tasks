# Generated by Django 2.2.6 on 2020-03-15 18:15

import datetime
from django.conf import settings
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Goal',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('goal', models.CharField(max_length=60)),
                ('initial_date', models.DateField(default=datetime.datetime(2020, 3, 15, 18, 15, 45, 276082, tzinfo=utc))),
                ('expiration_date', models.DateField()),
                ('status', models.CharField(choices=[('Completed', 'Completed'), ('Not completed', 'Not completed'), ('Cancelled', 'Cancelled'), ('In Progress', 'In Progress')], default='In Progress', max_length=24)),
                ('comments', models.CharField(max_length=200)),
                ('final_notes', models.CharField(max_length=200)),
                ('accounts', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'goal_table',
                'ordering': ['initial_date'],
            },
        ),
    ]
