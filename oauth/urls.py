import oauth.views as oauth_views
from django.urls import path

urlpatterns = [
    path('github_login', oauth_views.github_login, name='github_login'),
    path('github_check', oauth_views.github_check, name='github_check'),
    path('bind_email', oauth_views.bind_email, name='bind_email'),
]