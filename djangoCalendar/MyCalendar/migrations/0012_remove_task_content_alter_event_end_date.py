# Generated by Django 5.0.1 on 2024-01-04 15:48

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MyCalendar', '0011_alter_event_end_date_alter_task_priority'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='content',
        ),
        migrations.AlterField(
            model_name='event',
            name='end_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 4, 16, 48, 21, 349933, tzinfo=datetime.timezone.utc)),
        ),
    ]
