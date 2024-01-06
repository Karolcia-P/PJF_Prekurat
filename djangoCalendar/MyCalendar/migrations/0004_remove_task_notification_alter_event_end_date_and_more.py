# Generated by Django 5.0.1 on 2024-01-04 10:16

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MyCalendar', '0003_rename_date_event_start_date_calendar_color_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='notification',
        ),
        migrations.AlterField(
            model_name='event',
            name='end_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 4, 11, 16, 30, 751097, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='event',
            name='notification',
            field=models.TimeField(default=datetime.timedelta(seconds=3600)),
        ),
    ]