from django.db import models
from django.conf import settings


# Create your models here.
class Band(models.Model):
    name = models.CharField(max_length=200)
    needs = models.CharField(max_length=200)
    manager = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)


class Genre(models.Model):
    name = models.CharField(max_length=200)
    bands = models.ManyToManyField(Band, related_name="genre")
