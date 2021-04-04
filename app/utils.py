'''
this module provides necessary functions and auxiliary functions
WARNING!:
all functions not used to handle frontend request DIRECTLY should write here
'''
import app.times
import app.tokens
from app.models import User, Video
import jwt
import json
config = json.load(open('config.json', 'r'))
SECRET_KEY = config['SECRET_KEY'].encode('utf-8')



def is_registered(open_id):
    '''
    this function should check if a user registered by openID
    return: 1:yes 0:no
    '''
    user = User.objects.filter(open_id=open_id)
    return bool(user)


def get_registered_user(open_id):
    '''
    this function should a registered user's video list and count
    return: list, dic
    '''
    user = User.objects.get(open_id=open_id)
    video_list = Video.objects.filter(user=user).order_by('-pk')
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
    res_count_dictionary['video_count'] = user.video_count
    res_count_dictionary['name'] = user.name
    res_count_dictionary['sex'] = user.sex
    res_count_dictionary['fan'] = user.fan
    res_count_dictionary['follow'] = user.follow
    res_count_dictionary['head'] = user.head
    res_count_dictionary['bigHead'] = user.bigHead
    res_count_dictionary['city'] = user.city
    return res_video_list, res_count_dictionary


def update_registered_user(open_id, user_data, video_list, count_dictionary):
    '''
    this function should update a registered user
    '''
    user = User.objects.get(open_id=open_id)
    user.public_count = count_dictionary['public_count']
    user.friend_count = count_dictionary['friend_count']
    user.private_count = count_dictionary['private_count']
    user.video_count = count_dictionary['all_count']
    user.name = user_data['name']
    if user_data['sex'] == 'F':
        user.sex = 1
    else:
        if user_data['sex'] == 'M':
            user.sex = 0
        else:
            user.sex = None
    user.fan = user_data['fan']
    user.follow = user_data['follow']
    user.head = user_data['head']
    user.bigHead = user_data['bigHead']
    user.city = user_data['city']
    user.save()
    new_video_list = []
    old_video_list = Video.objects.filter(user=user)
    for video in video_list:
        new_video_list.append(video['photo_id'])
    for video in old_video_list:
        if str(video.photo_id) not in new_video_list:
            video.delete()
    for i, _ in enumerate(new_video_list):
        if not bool(Video.objects.filter(photo_id=new_video_list[i])):
            video = Video(
                user=user,
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
    '''
    this function should create a user in User model and his works in Video
    '''
    if user_data["sex"] == 'F':
        sex = 1
    else:
        if user_data["sex"] == 'M':
            sex = 0
        else:
            sex = None
    new_user = User(open_id=open_id,
                    public_count=count_dictionary['public_count'],
                    friend_count=count_dictionary['friend_count'],
                    private_count=count_dictionary['private_count'],
                    video_count=count_dictionary['all_count'],
                    name=user_data['name'],
                    sex=sex,
                    fan=user_data['fan'],
                    follow=user_data['follow'],
                    head=user_data['head'],
                    bigHead=user_data['bigHead'],
                    city=user_data['city'])
    new_user.save()
    for video in video_list:
        new_video = Video(user=new_user,
                          photo_id=video['photo_id'],
                          caption=video['caption'],
                          cover=video['cover'],
                          play_url=video['play_url'],
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
    res = 0
    target = User.objects.get(open_id=open_id)
    video_list = target.video.all()
    for video in video_list:
        res += video.like_count
    return res


def get_total_comment_count(open_id):
    """
    this function should return the total_comment_count of the user
    return: total_comment_count
    """
    res = 0
    target = User.objects.get(open_id=open_id)
    video_list = target.video.all()
    for video in video_list:
        res += video.comment_count
    return res


def get_total_view_count(open_id):
    """
    this function should return the total_view_count of the user
    return: total_view_count
    """
    res = 0
    target = User.objects.get(open_id=open_id)
    video_list = target.video.all()
    for video in video_list:
        res += video.view_count
    return res


def store_token(open_id, access_token, refresh_token):
    """
    this function should store the access and refresh token
    (regardless of initialize or update)
    """
    user = User.objects.get(open_id=open_id)
    user.access_token = app.tokens.encode_token(access_token)
    user.refresh_token = app.tokens.encode_token(refresh_token)
    user.save()


def get_token(open_id):
    """
    this function returns the tokens of a user
    return: access_token, refresh_token
    """
    user = User.objects.get(open_id=open_id)
    access_token = app.tokens.decode_token(user.access_token)
    refresh_token = app.tokens.decode_token(user.refresh_token)
    return access_token, refresh_token


def encoding_message(message):
    """
    this function is for encoding data using jwt to pass to frontend
    """
    encode_jwt = jwt.encode(message, SECRET_KEY, algorithm='HS256')
    encode_str = str(encode_jwt, 'utf-8')
    return encode_str


def decoding_message(token):
    """
    this function is for decoding jwt into json
    """
    message = jwt.decode(token, SECRET_KEY, algorithm='HS256')
    return message
