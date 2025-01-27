# Generated by Django 5.0.1 on 2024-01-04 15:10

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MyCalendar', '0010_alter_event_end_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='end_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 4, 16, 10, 33, 741053, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='task',
            name='priority',
            field=models.IntegerField(choices=[(1, 'High Priority'), (2, 'Medium Priority'), (3, 'Low Priority')]),
        ),
    ]
