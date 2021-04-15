'''
this is a url configuration for analyseFans
'''

from django.urls import path

from . import views

urlpatterns = [
    path('globalhour', views.get_fans_info)
]
