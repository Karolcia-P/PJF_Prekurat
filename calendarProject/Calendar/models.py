from django.db import models
class calendar_event(models.Model):
    tytul = models.CharField(max_length=200)
    data = models.DateField()
# Create your models here.
