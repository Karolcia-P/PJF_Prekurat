# Generated by Django 5.0.1 on 2024-01-13 20:38

import datetime
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MyCalendar', '0018_remove_project_reminder_date_alter_event_end_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='end_time',
            field=models.TimeField(default=datetime.datetime(2024, 1, 13, 21, 38, 3, 378750, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AddField(
            model_name='event',
            name='start_time',
            field=models.TimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='event',
            name='end_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='event',
            name='start_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
