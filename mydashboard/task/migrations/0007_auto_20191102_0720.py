# Generated by Django 2.2.6 on 2019-11-02 13:20

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0006_auto_20191101_1551'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='initial_date',
            field=models.DateField(default=datetime.datetime(2019, 11, 2, 13, 20, 52, 790937, tzinfo=utc)),
        ),
    ]