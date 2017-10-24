from django.db import models
from django.conf import settings
#from concert.models import Concert
#Concert = apps.get_model(app_label='concert', model_name='Concert')

class Genre(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Band(models.Model):
    name = models.CharField(max_length=200)
    manager = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    genres = models.ManyToManyField(Genre, related_name="bands")
    streaming_popularity = models.IntegerField(default=0)
    albums_sold = models.IntegerField(default=0)
    #earlier_concerts = models.ForeignKey('concert.Concert')

    def __str__(self):
        genres = self.genres.all()
        s = ""
        for i in range(genres.count() - 1):
            s += str(genres[i]) + ", "
        s += str(genres[genres.count() - 1])
        return self.name + " - " + s
