'''
this module provides necessary functions and auxiliary functions
WARNING!:
all functions not used to handle frontend request DIRECTLY should write here

FUNCTION TEMPLATE for view:
    if request.method == 'GET':
        try:
            open_id = request.GET.get('open_id')
        except Exception:
            return app.utils.gen_response(400, traceback.format_exc())
    return app.utils.gen_response(405)
    if request.method == 'POST':
        try:
            ret = request.body
            ret = json.loads(ret.decode('utf-8'))
        except Exception:
            return app.utils.gen_response(400, traceback.format_exc())
    return app.utils.gen_response(405)
'''
import json
from django.http import JsonResponse
import app.times
import app.tokens
from app.models import User, Video, Analyse, AnalyseHour, Warn

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
        else:
            video = Video.objects.get(photo_id=new_video_list[i])
            video.caption = video_list[i]['caption']
            video.cover = video_list[i]['cover']
            video.play_url = video_list[i]['play_url']
            video.create_time = app.times.timestamp2string(
                video_list[i]['create_time'])  # timestamp2str
            video.like_count = video_list[i]['like_count']
            video.comment_count = video_list[i]['comment_count']
            video.view_count = video_list[i]['view_count']
            video.pending = video_list[i]['pending']
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


def get_videos_by_timestamp(open_id, before_timestamp, after_timestamp):
    """
    this function should return the videos
    based on the before and after timestamp
    return: videos
    """
    user = User.objects.get(open_id=open_id)
    video_list = user.video.all().order_by('-create_time')
    videos = []
    for video in video_list:
        if int(before_timestamp) <= app.times.datetime2timestamp(
                video.create_time) <= int(after_timestamp):
            videos.append(video)
    return videos


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


def gen_response(code: int, data=None):
    """
    this function is for generating web response
    """
    return JsonResponse({'code': code, 'data': data}, status=code)


def get_all_open_id():
    """
    this function should return all users' open_id
    """
    open_id_list = []
    for user in User.objects.all():
        open_id_list.append(user.open_id)
    return open_id_list


def analyse_hour_data(open_id, video_list, time):
    """
    本函数接口用于把每小时的数据放入AnalyseHour表中
    """
    for vid in video_list:
        photo_id = vid.get("photo_id")
        video_object = Video.objects.get(photo_id=photo_id)
        data = AnalyseHour.objects.create(
            video=video_object,
            user_id=open_id,
            sum_time=time,
            total_view_count=vid.get("view_count"),
            total_comment_count=vid.get("comment_count"),
            total_like_count=vid.get("like_count"))
        data.save()


def analyse_daily_data(open_id, video_list, time):
    """
    本函数接口用于把每天的数据放入Analyse表中
    """
    for vid in video_list:
        photo_id = vid.get("photo_id")
        video_object = Video.objects.get(photo_id=photo_id)
        data = Analyse.objects.create(
            video=video_object,
            user_id=open_id,
            sum_time=time,
            total_view_count=vid.get("view_count"),
            total_comment_count=vid.get("comment_count"),
            total_like_count=vid.get("like_count"))
        data.save()


def is_administrator(open_id):
    """
    本函数用于判断一个人的身份是否为管理员
    """
    user = User.objects.get(open_id=open_id)
    return user.identity


def store_flow(open_id, one_day_before_time, one_hour_before_time,
               now_time):
    """
    本函数用于存储一个用户的流量预警变化
    """
    user = User.objects.get(open_id=open_id)
    limit = user.limit / 100
    analyse_list = AnalyseHour.objects.filter(
        user_id=open_id).order_by('sum_time')
    one_day_count = {'like_count': 0, 'comment_count': 0, 'view_count': 0}
    one_hour_count = {'like_count': 0, 'comment_count': 0, 'view_count': 0}
    now_count = {'like_count': 0, 'comment_count': 0, 'view_count': 0}
    for analyse in analyse_list:
        if one_day_before_time == app.times.datetime2timestamp(
                analyse.sum_time):
            one_day_count['like_count'] += analyse.total_like_count
            one_day_count['comment_count'] += analyse.total_comment_count
            one_day_count['view_count'] += analyse.total_view_count

        if one_hour_before_time == app.times.datetime2timestamp(
                analyse.sum_time):
            one_hour_count['like_count'] += analyse.total_like_count
            one_hour_count['comment_count'] += analyse.total_comment_count
            one_hour_count['view_count'] += analyse.total_view_count

        if now_time == app.times.datetime2timestamp(analyse.sum_time):
            now_count['like_count'] += analyse.total_like_count
            now_count['comment_count'] += analyse.total_comment_count
            now_count['view_count'] += analyse.total_view_count

    if one_day_count['like_count'] == 0 \
            or one_hour_count['like_count'] == 0:
        return

    likes_change = now_count["like_count"] - one_hour_count['like_count']
    comments_change = \
        now_count["comment_count"] - one_hour_count['comment_count']
    views_change = now_count["view_count"] - one_hour_count['view_count']

    likes_before = now_count["like_count"] - one_day_count['like_count']
    comments_before = \
        now_count["comment_count"] - one_day_count['comment_count']
    views_before = now_count["view_count"] - one_day_count['view_count']

    if likes_change > limit * likes_before \
            or comments_change > limit * comments_before \
            or views_change > limit * views_before:
        data = Warn.objects.create(
            user=user,
            likes_change=likes_change,
            comments_change=comments_change,
            views_change=views_change,
            likes_before=likes_before,
            comments_before=comments_before,
            views_before=views_before,
            warn_time=app.times.timestamp2datetime(now_time))
        data.save()


def get_flow(open_id):
    """
    本函数接口通过用户的open_id得到存储在数据库中的所有流量预警
    """
    user = User.objects.get(open_id=open_id)
    flows = Warn.objects.filter(user=user).order_by('-warn_time')
    flow_list = []
    for flow in flows:
        flow_list.append({
            'like_change':
                flow.likes_change,
            'comments_change':
                flow.comments_change,
            'views_change':
                flow.views_change,
            'likes_before':
                flow.likes_before,
            'comments_before':
                flow.comments_before,
            'views_before':
                flow.views_before,
            'warn_time':
                app.times.datetime2timestamp(flow.warn_time)
        })
    return flow_list


def update_limit(open_id, limit):
    """
    本接口用于更改用户设定的流量预警阈值
    """
    user = User.objects.get(open_id=open_id)
    user.limit = int(limit)
    user.save()
