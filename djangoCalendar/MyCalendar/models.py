from django.db import models
from django.contrib.auth.models import User

class Calendar(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

class Event(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    date = models.DateTimeField()
    calendar = models.ForeignKey(Calendar, on_delete=models.CASCADE)
    notification = models.BooleanField(default=False)

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    start_date = models.DateField()
    priority = models.IntegerField()
    notification = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)

class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField()
    reminder_date = models.DateField(null=True, blank=True)
    completed = models.BooleanField(default=False)
