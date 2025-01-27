# Generated by Django 5.0.1 on 2024-01-06 15:53

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MyCalendar', '0015_alter_event_end_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='reminder_displayed',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='event',
            name='end_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 6, 16, 53, 32, 883805, tzinfo=datetime.timezone.utc)),
        ),
    ]
