'''
this module provides necessary functions and auxiliary functions
WARNING!:
all functions not used to handle frontend request DIRECTLY should write here
'''
from app.models import *
import app.times


def is_registered(open_id):
    '''
    this fuction should check if a user registered by openID
    return: 1:yes 0:no
    3.24: untest
    '''
    user = User.objects.filter(open_id=open_id)
    return bool(user)


def get_registered_user(open_id):
    '''
    this fuction should a registered user's video list and count
    return: list, dic
    3.24: untest
    '''
    user = User.objects.get(open_id=open_id)
    video_list = Video.objects.filter(user=open_id).order_by('-pk')
    res_video_list = []
    for video in video_list:
        video_dictionary = {}
        video_dictionary['photo_id'] = video.photo_id
        video_dictionary['caption'] = video.caption
        video_dictionary['cover'] = video.cover
        video_dictionary['play_url'] = video.play_url
        video_dictionary['create_time'] = app.times.datetime2timestamp(
            video.create_time)  # datetime2timestamp
        video_dictionary['like_count'] = video.like_count
        video_dictionary['comment_count'] = video.comment_count
        video_dictionary['view_count'] = video.view_count
        video_dictionary['pending'] = video.pending
        res_video_list.append(video_dictionary)
    res_count_dictionary = {}
    res_count_dictionary['open_id'] = open_id
    res_count_dictionary['public_count'] = user.public_count
    res_count_dictionary['friend_count'] = user.friend_count
    res_count_dictionary['private_count'] = user.private_count
    res_count_dictionary['all_count'] = user.all_count
    return res_video_list, res_count_dictionary


def update_registered_user(open_id, user_data, video_list, count_dictionary):
    # 数据库还需要更新user_data，本函数需要更新一下
    '''
    this function should update a registered user
    3.24: untest
    '''
    user = User.objects.get(open_id=open_id)
    user.public_count = count_dictionary['public_count']
    user.friend_count = count_dictionary['friend_count']
    user.private_count = count_dictionary['private_count']
    user.all_count = count_dictionary['all_count']
    new_video_list = []
    old_video_list = Video.objects.filter(user=open_id)
    for video in video_list:
        new_video_list.append(video['photo_id'])
    for video in old_video_list:
        if str(video.photo_id) not in new_video_list:
            video.delete()
    for i, _ in enumerate(new_video_list):
        if not bool(Video.objects.filter(photo_id=new_video_list[i])):
            video = Video(
                user=open_id,
                photo_id=video_list[i]['photo_id'],
                caption=video_list[i]['caption'],
                cover=video_list[i]['cover'],
                play_url=video_list[i]['play_url'],
                create_time=app.times.timestamp2string(
                    video_list[i]['create_time']),  # timestamp2str
                like_count=video_list[i]['like_count'],
                comment_count=video_list[i]['comment_count'],
                view_count=video_list[i]['view_count'],
                pending=video_list[i]['pending'])
            video.save()


def initialize_new_user(open_id, user_data, video_list, count_dictionary):
    # 还需要向数据库中存入user_data，本函数需要更新一下
    '''
    this function should create a user in User model and his works in Video
    3.24: untest
    '''
    new_user = User(open_id=open_id,
                    public_count=count_dictionary['public_count'],
                    friend_count=count_dictionary['friend_count'],
                    private_count=count_dictionary['private_count'],
                    all_count=count_dictionary['all_count'])
    new_user.save()
    for video in video_list:
        new_video = Video(user=open_id,
                          photo_id=video['photo_id'],
                          caption=video['caption'],
                          cover=['cover'],
                          play_url=['play_url'],
                          create_time=app.times.timestamp2string(
                              video['create_time']),
                          like_count=video['like_count'],
                          comment_count=video['comment_count'],
                          view_count=video['view_count'],
                          pending=video['pending'])
        new_video.save()


def get_total_like_count(open_id):
    """
    this function should return the total_like_count of the user
    return: total_like_count
    """


def get_total_comment_count(open_id):
    """
    this function should return the total_comment_count of the user
    return: total_comment_count
    """


def get_total_view_count(open_id):
    """
    this function should return the total_view_count of the user
    return: total_view_count
    """


def store_token(open_id, access_token, refresh_token):
    """
    this function should store the access and refresh token
    (regardless of initialize or update)
    """
