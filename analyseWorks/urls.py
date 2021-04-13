'''
this is a url configuration for manageWorks
'''

from django.urls import path

from . import views

urlpatterns = [
    path('single', views.get_videos_info_by_time),
    path('global_day', views.g)
]
