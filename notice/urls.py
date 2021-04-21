'''
this is a url configuration for manageWorks
'''

from django.urls import path

from . import views

urlpatterns = [
    path('user', views.get_notice_user),
    path('admin', views.operate_notice_admin)
]
