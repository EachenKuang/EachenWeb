from django.shortcuts import render
from django.http import JsonResponse
from movie.models import Movie
from django.core import serializers
# Create your views here.


def get_list(request):

    movie_all_list = Movie.objects.values()
    # movie_all_list = serializers.serialize("list", movie_all_list)
    data = dict()
    data['movieList'] = list(movie_all_list)
    return JsonResponse(data)