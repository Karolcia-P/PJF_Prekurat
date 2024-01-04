from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Calendar(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=7, default='#0000FF')

class Event(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(default=timezone.now() + timezone.timedelta(hours=1))
    calendar = models.ForeignKey(Calendar, on_delete=models.CASCADE)
    notification = models.DateTimeField(default=timezone.now() - timezone.timedelta(hours=1))

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    content = models.TextField()
    start_date = models.DateField()
    priority = models.IntegerField()
    completed = models.BooleanField(default=False)

class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    reminder_date = models.DateField(null=True, blank=True)
    completed = models.BooleanField(default=False)
