'''
this is a url configuration for login
'''

from django.urls import path

from . import views

urlpatterns = [
    path('time', views.get_videos_in_time),
]
