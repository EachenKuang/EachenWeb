from django.urls import path
from movie import views

urlpatterns = [
    path('movie_list', views.get_list),
]
