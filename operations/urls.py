from django.urls import path

from . import views
'''
main url: /api/test/
method: GET
path('user', views.operate_user)
    receive:
        add: 0/1/404/any other int
            0: delete a user
            1: create a user
            404: create FAKE analysis for a user
            any other int: do nothing
        open_id(choice): when add=0/1/404, needed
        name(choice): when add=0/1, needed
    return:
        all users infos AFTER operations
path('admin', views.set_admin)
    receive:
        add: 0/1
            0: set to customer
            1: set to admin
        open_id
    return:
        all users infos AFTER operations
path('user_analysis', views.user_analysis)
    receive:
        open_id
    return:
        all analysis belonged
path('video_analysis', views.video_analysis
    receive:
        photo_id
    return:
        all analysis belonged
path('video_analysis_hour', views.video_analysis_hour)
    receive:
        photo_id
    return:
        all analysisHour belonged

path('video_label', views.video_label)
    receive:
        open_id
        add=0/other
    return:
        user info
        label
'''
urlpatterns = [
    path('user', views.operate_user),
    path('admin', views.set_admin),
    path('user_analysis', views.user_analysis),
    path('video_analysis', views.video_analysis),
    path('video_analysis_hour', views.video_analysis_hour),
    path('video_label', views.video_label)
]
