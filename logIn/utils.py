'''
this module provides necessary functions and auxiliary functions
WARNING:
all fucntions not used to handle frontend request DIRECTLY should write here
'''
from app.models import User
from app.models import Video


def initialize_new_customer(open_id, video_list, count_dictionary):
    '''
    this function should create a user in User model and his works in Video
    untest: 3.24
    '''
    new_user = User(_open_id=open_id,
                    _public_count=count_dictionary['public_count'],
                    _friend_count=count_dictionary['friend_count'],
                    _private_count=count_dictionary['private_count'],
                    _all_count=count_dictionary['all_count'])
    new_user.save()
    for video in video_list:
        new_video = Video(_user=new_user,
                          _photo_id=video['photo_id'],
                          _caption=video['caption'],
                          _cover=['cover'],
                          _play_url=['play_url'],
                          _create_time=video['create_time'],
                          _like_count=video['like_count'],
                          _comment_count=video['comment_count'],
                          _view_count=video['view_count'],
                          _pending=video['pending'])
        new_video.save()
