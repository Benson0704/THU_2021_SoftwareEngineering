"""
this is a module for getting the information of videos and labels
"""
import json
import app.utils
import app.times
import app.api
from app.models import User, Video, Label


def get_video_time_sort(request):
    """
    this function should respond to the get video request
    """
    if request.method == 'GET':
        ret = request.body
        try:
            ret = json.loads(ret.decode('utf-8'))
        except ValueError:
            return app.utils.gen_response(
                400, app.utils.encoding_message(400, 'not json'))
        try:
            open_id = ret['open_id']
            begin_timestamp = ret['begin_timestamp']
            end_timestamp = ret['term_timestamp']
            count_per_page = ret['count_per_page']
            page = ret['page']
            app.api.manage_data(open_id)
            user = User.objects.get(open_id=open_id)
            videos = user.video.all().order_by('-create_time')
            video_list = []
            for video in videos:
                if begin_timestamp <= app.times.datetime2timestamp(
                        video.create_time) <= end_timestamp:
                    video_list.append(video)
            return_list = []
            for i, video in enumerate(video_list):
                if count_per_page * (page - 1) <= i < count_per_page * page:
                    return_list.append({
                        'photo_id':
                        video_list[i].photo_id,
                        'caption':
                        video_list[i].caption,
                        'cover':
                        video_list[i].cover,
                        'play_url':
                        video_list[i].play_url,
                        'create_time':
                        app.times.datetime2timestamp(
                            video_list[i].create_time),
                        'like_count':
                        video_list[i].like_count,
                        'comment_count':
                        video_list[i].comment_count,
                        'view_count':
                        video_list[i].view_count,
                        'pending':
                        video_list[i].pending,
                        'labels':
                        video_list[i].labels.split('_&_')
                    })
            return app.utils.gen_response(
                200, app.utils.encoding_message(200, return_list))
        except ValueError:
            return app.utils.gen_response(
                400, app.utils.encoding_message(400, 'json content error'))
    else:
        return app.utils.gen_response(
            405, app.utils.encoding_message(405, 'no\
             such method'))


def get_label_list(request):
    """
    this function should respond to the requests relating to labels
    """
    if request.method == 'GET':
        ret = request.body
        try:
            ret = json.loads(ret.decode('utf-8'))
        except ValueError:
            return app.utils.gen_response(
                400, app.utils.encoding_message(400, 'not json'))
        try:
            open_id = ret['open_id']
            app.api.manage_data(open_id)
            user = User.objects.get(open_id=open_id)

        except ValueError:
            return app.utils.gen_response(
                400, app.utils.encoding_message(400, 'json content error'))
    elif request.method == 'POST':
        ret = request.body
        try:
            ret = json.loads(ret.decode('utf-8'))
        except ValueError:
            return app.utils.gen_response(
                400, app.utils.encoding_message(400, 'not json'))
        try:
            open_id = ret['open_id']
        except ValueError:
            return app.utils.gen_response(
                400, app.utils.encoding_message(400, 'json content error'))
    else:
        return app.utils.gen_response(
            405,
            app.utils.encoding_message(405, 'no\
             such method '))
