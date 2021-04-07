'''
this is a url configuration for manageWorks
'''

from django.urls import path

from . import views

urlpatterns = [
    path('single', views.get_videos_in_time),
    path('global_day', views.g)
]
