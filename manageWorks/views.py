"""
this is a module for getting the information of videos and labels
"""
import json
import app.utils
import app.times
import app.api
from app.models import User, Video, Label
from django.views.decorators.csrf import csrf_exempt


def get_video_time_sort(request):
    """
    this function should respond to the get video request
    """
    if request.method == 'GET':
        ret = request.body
        try:
            ret = json.loads(ret.decode('utf-8'))
        except:
            return app.utils.gen_response(400, 'not json')
        try:
            open_id = ret['open_id']
            begin_timestamp = ret['begin_timestamp']
            end_timestamp = ret['term_timestamp']
            # app.api.manage_data(open_id)
            user = User.objects.get(open_id=open_id)
            videos = user.video.all().order_by('-create_time')
            video_list = []
            for video in videos:
                if begin_timestamp <= app.times.datetime2timestamp(
                        video.create_time) <= end_timestamp:
                    video_list.append(video)
            return_list = []
            for i, video in enumerate(video_list):
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
                    app.times.datetime2timestamp(video_list[i].create_time),
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
            return app.utils.gen_response(200, return_list)
        except:
            return app.utils.gen_response(400, 'json content error')
    else:
        return app.utils.gen_response(405, 'no such method')


@csrf_exempt
def get_label_list(request):
    """
    this function should respond to the requests relating to labels
    """
    if request.method == 'GET':
        ret = request.body
        try:
            ret = json.loads(ret.decode('utf-8'))
        except:
            return app.utils.gen_response(400, 'not json')
        try:
            open_id = ret['open_id']
            # app.api.manage_data(open_id)
            user = User.objects.get(open_id=open_id)
            return_list = []
            labels = user.Label.objects.all()
            for label in labels:
                return_list.append({
                    'label': label.label_name,
                    'num': label.num
                })
            return app.utils.gen_response(200, return_list)
        except:
            return app.utils.gen_response(400, 'json content error')
    elif request.method == 'POST':
        ret = request.body
        try:
            ret = json.loads(ret.decode('utf-8'))
        except:
            return app.utils.gen_response(400, 'not json')
        try:
            try:
                open_id = ret['open_id']
                target_label = ret['label']
                photo_id = ret['photo_id']
                add = ret['add']
                # app.api.manage_data(open_id)
                user = User.objects.get(open_id=open_id)
            except:
                return app.utils.gen_response(110, 'user')
            if add == 1:
                try:
                    label = user.Label.get(label_name=target_label)
                    label.num += 1
                    label.save()
                except:
                    try:
                        label = Label(user=user, label_name=target_label)
                        label.num += 1
                        label.save()
                    except:
                        return app.utils.gen_response(113, 'new labels')
                try:
                    video = Video.objects.get(photo_id=photo_id)
                    video.labels = video.labels + target_label + '_&_'
                    video.save()
                except:
                    return app.utils.gen_response(100, 'video')

            else:
                try:
                    label = user.Label.get(label_name=target_label)
                    label.num -= 1
                    if label.num <= 0:
                        label.delete()
                    else:
                        label.save()
                    video = Video.objects.get(photo_id=photo_id)
                    video.labels = video.labels.replace(
                        target_label + '_&_', '')
                    video.save()
                except:
                    return app.utils.gen_response(102, 'videos and labels')
            return app.utils.gen_response(2010, 'here')
        except:
            return app.utils.gen_response(
                40, '{}json content error'.format(str(ret)))
    else:
        return app.utils.gen_response(405, 'no such method ')
