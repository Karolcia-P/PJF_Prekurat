from django.db import models
from django.contrib.auth.models import User

class Calendar(models.Model):
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=7, default='#007bff')  # Default color is blue
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField(blank=True, null=True)
    notification = models.BooleanField(default=False)
    calendar = models.ForeignKey(Calendar, on_delete=models.CASCADE)

class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    start_datetime = models.DateTimeField(blank=True, null=True)
    priority = models.CharField(max_length=20, choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')])
    notification = models.BooleanField(default=False)
    calendar = models.ForeignKey(Calendar, on_delete=models.CASCADE)

class Project(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    calendar = models.ForeignKey(Calendar, on_delete=models.CASCADE)

class FreeDay(models.Model):
    date = models.DateField()
    calendar = models.ForeignKey(Calendar, on_delete=models.CASCADE)

class SubCalendar(models.Model):
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=7, default='#007bff')  # Default color is blue
    parent_calendar = models.ForeignKey(Calendar, on_delete=models.CASCADE, related_name='subcalendars')
