# Generated by Django 5.0.1 on 2024-01-04 12:51

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MyCalendar', '0006_alter_event_end_date_alter_event_start_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='end_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 4, 13, 51, 35, 156229, tzinfo=datetime.timezone.utc)),
        ),
    ]
