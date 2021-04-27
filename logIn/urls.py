'''
this is a url configuration for login
'''

from django.urls import path

from . import views

urlpatterns = [
    path('home', views.get_user_info_by_code),
    path('home/id', views.get_user_info_by_id),
    path('home/add',views.add_test),
    path('home/delete',views.delete_test)
]
