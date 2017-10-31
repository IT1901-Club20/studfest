from django.db import models
from django.conf import settings


class Genre(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Band(models.Model):
    name = models.CharField(max_length=200)
    manager = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    genres = models.ManyToManyField(Genre, related_name="bands")
    image_filename = models.CharField(max_length=210, default="catplaceholder.jpg")
    bio_text = models.CharField(max_length=1400, default="No bio yet :(")
    streaming_popularity = models.IntegerField(default=0)
    albums_sold = models.IntegerField(default=0)

    def __str__(self):
        genres = self.genres.all()
        s = ""
        for i in range(genres.count() - 1):
            s += str(genres[i]) + ", "
        s += str(genres[genres.count() - 1])
        return self.name + " - " + s
