'''
this is a url configuration for share
'''

from django.urls import path

from . import views

urlpatterns = [
    path('add', views.add_share),
    path('delete', views.delete_share),
    path('sharing', views.get_my_sharing_user),
    path('shared', views.get_user_share_to_me)
]
