from django.db import models

# Create your models here.


class Movie(models.Model):
    mid = models.IntegerField()
    movieName = models.TextField()
    movieImg = models.TextField()
    movieEvaluate = models.TextField()
    score = models.FloatField()

