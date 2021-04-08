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
        try:
            open_id = request.GET.get('open_id')
            begin_timestamp = request.GET.get('begin_timestamp')
            term_timestamp = request.GET.get('term_timestamp')
            app.api.manage_data(open_id)
            video_list = app.utils.get_videos_by_timestamp(
                open_id, begin_timestamp, term_timestamp)
            return_list = []
            for i, _ in enumerate(video_list):
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
            return app.utils.gen_response(200, {
                'video_count': len(return_list),
                'video_list': return_list
            })
        except:
            return app.utils.gen_response(400)
    else:
        return app.utils.gen_response(405)


def get_label_list(request):
    """
    this function should respond to the requests relating to labels
    """
    if request.method == 'GET':
        try:
            open_id = request.GET.get('open_id')
            app.api.manage_data(open_id)
            user = User.objects.get(open_id=open_id)
            labels = user.label.all()
            return_list = []
            for label in labels:
                return_list.append({
                    'label': label.label_name,
                    'num': label.num
                })
            return app.utils.gen_response(200, {'label_list': return_list})
        except:
            return app.utils.gen_response(400)
    elif request.method == 'POST':
        ret = request.body
        try:
            ret = json.loads(ret.decode('utf-8'))
        except:
            return app.utils.gen_response(400)
        try:
            open_id = ret['open_id']
            target_label = ret['label']
            photo_id = ret['photo_id']
            add = ret['add']
            app.api.manage_data(open_id)
            user = User.objects.get(open_id=open_id)
            if add:
                try:
                    label = user.label.get(label_name=target_label)
                    label.num += 1
                    label.save()
                except:
                    label = Label(user=user, label_name=target_label)
                    label.num += 1
                    label.save()
                video = Video.objects.get(photo_id=photo_id)
                video.labels = video.labels + target_label + '_&_'
                video.save()
            else:
                label = user.label.get(label_name=target_label)
                label.num -= 1
                if label.num <= 0:
                    label.delete()
                else:
                    label.save()
                video = Video.objects.get(photo_id=photo_id)
                video.labels = video.labels.replace(target_label + '_&_', '')
                video.save()
            return app.utils.gen_response(201)
        except:
            return app.utils.gen_response(400)
    else:
        return app.utils.gen_response(405)
