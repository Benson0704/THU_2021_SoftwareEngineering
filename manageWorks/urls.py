'''
this is a url configuration for login
'''

from django.urls import path

from . import views

urlpatterns = [
    path('time', views.video),
    path('label', views.label),
]
