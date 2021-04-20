'''
this is a url configuration for manageWorks
'''

from django.urls import path

from . import views

urlpatterns = [
    path('user', views.operate_feedback_user),
    path('admin', views.operate_feedback_admin)
]
