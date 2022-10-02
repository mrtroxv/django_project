from django.db import models


class Song(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    author = models.CharField(max_length=255, default="null")
    type = models.CharField(max_length=255)
    image_url = models.CharField(max_length=255)
    file_url = models.CharField(max_length=255)
    rating = models.FloatField()
    tag = models.CharField(max_length=255, default="null")
    time_created = models.DateTimeField(null=True)
    time_updated = models.DateTimeField(null=True)


# Create your models here.

# Create your models here.
