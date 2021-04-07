'''
this is a url configuration for login
'''

from django.urls import path

from . import views

urlpatterns = [
    path('home', views.oauth_callback),
    path('home/id', views.get_user_info)
]
