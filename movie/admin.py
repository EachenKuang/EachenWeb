from django.contrib import admin
from movie.models import Movie

# Register your models here.
@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('id', 'movieName', 'movieImg', 'movieEvaluate', 'score')
