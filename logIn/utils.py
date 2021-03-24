'''
this module provides necessary functions and auxiliary functions
WARNING:
all fucntions not used to handle frontend request DIRECTLY should write here
'''
from app.models import User
from app.models import Video


def is_registered(open_id):
    '''
    this fuction should check if a user registered by openID
    return: 1:yes 0:no
    3.24: untest
    '''
    user = User.objects.filter(_open_id=open_id)
    return bool(user)


def get_registered_user(open_id):
    '''
    this fuction should a registered user's video list and count
    return: list, dic
    3.24: untest
    '''
    user = User.objects.get(_open_id=open_id)
    video_list = Video.objects.filter(_user=user)
    res_video_list = []
    for video in video_list:
        video_dictionary = {}
        video_dictionary['photo_id'] = video._photo_id
        video_dictionary['caption'] = video._caption
        video_dictionary['cover'] = video._cover
        video_dictionary['play_url'] = video._play_url
        video_dictionary['create_time'] = video._create_time
        video_dictionary['like_count'] = video._like_count
        video_dictionary['comment_count'] = video._comment_count
        video_dictionary['view_count'] = video._view_count
        video_dictionary['pending'] = video._pending
        res_video_list.append(video_dictionary)
    res_count_dictionary = {}
    res_count_dictionary['open_id'] = open_id
    res_count_dictionary['public_count'] = user._public_count
    res_count_dictionary['friend_count'] = user._friend_count
    res_count_dictionary['private_count'] = user._private_count
    res_count_dictionary['all_count'] = user._all_count
    return res_video_list, res_count_dictionary


def update_registered_user(open_id, video_list, count_dictionary):
    '''
    this fuction should update a registered user
    3.24: untest
    '''
    user = User.objects.get(_open_id=open_id)
    user._public_count = count_dictionary['public_count']
    user._friend_count = count_dictionary['friend_count']
    user._private_count = count_dictionary['private_count']
    user._all_count = count_dictionary['all_count']
    new_video_list = []
    old_video_list = Video.objects.filter(_user=user)
    for video in video_list:
        new_video_list.append(video['photo_id'])
    for video in old_video_list:
        if str(video._photo_id) not in new_video_list:
            video.delete()
    for i, _ in enumerate(new_video_list):
        if not bool(Video.objects.filter(_photo_id=new_video_list[i])):
            video = Video(_user=user,
                          _photo_id=video_list[i]['photo_id'],
                          _caption=video_list[i]['caption'],
                          _cover=video_list[i]['cover'],
                          _play_url=video_list[i]['play_url'],
                          _create_time=video_list[i]['create_time'],
                          _like_count=video_list[i]['like_count'],
                          _comment_count=video_list[i]['comment_count'],
                          _view_count=video_list[i]['view_count'],
                          _pending=video_list[i]['pending'])
            video.save()


def initialize_new_user(open_id, video_list, count_dictionary):
    '''
    this function should create a user in User model and his works in Video
    3.24: untest
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
