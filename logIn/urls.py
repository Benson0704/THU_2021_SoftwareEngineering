'''
this is a url configuration for login
'''

from django.urls import path

from . import views

urlpatterns = [
    path('oauth', views.oauth),
    path('oauth/callback', views.oauth_callback),
]
