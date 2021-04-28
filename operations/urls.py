from django.urls import path

from . import views

urlpatterns = [
    path('user'.views.operate_user),
    path('admin', views.set_admin),
    path('user_analysis', views.user_analysis),
    path('video_analysis', views.video_analysis)
]
