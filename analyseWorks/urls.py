'''
this is a url configuration for manageWorks
'''

from django.urls import path

from . import views

urlpatterns = [
    path('single', views.get_videos_info_by_time),
    path('globalday', views.get_all_videos_info)
]
