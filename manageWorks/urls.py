'''
this is a url configuration for login
'''

from django.urls import path

from . import views

urlpatterns = [
    path('time', views.get_video_time_sort),
    path('label', views.get_label_list),
]
