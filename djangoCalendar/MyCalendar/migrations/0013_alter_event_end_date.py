# Generated by Django 5.0.1 on 2024-01-04 16:26

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MyCalendar', '0012_remove_task_content_alter_event_end_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='end_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 4, 17, 26, 12, 2115, tzinfo=datetime.timezone.utc)),
        ),
    ]