"""
this is a module for analyse the information of videos and labels
"""

import json
import app.utils
import app.times
import app.api
from app.models import User, Video, Label, Analyse


def get_videos_info_by_time(request):
    if request.method == 'GET':
        try:
            open_id = request.GET.get('open_id')
            photo_id = request.GET.get('photo_id')
            begin_timestamp = request.GET.get('begin_timestamp')
            term_timestamp = request.GET.get('term_timestamp')
        except:
            return app.utils.gen_response(400)
        video = Video.objects.get(photo_id=photo_id)
        analyse_list = []
        analyse_list = Analyse.objects.filter(
            video=video).order_by('-sum_time')
        res = {}
        res['photo_id'] = photo_id
        res['caption'] = video.caption
        res['cover'] = video.cover
        res['play_url'] = video.play_url
        res['create_time'] = video.create_time
        res['pending'] = False
        res['like_count'] = video.like_count
        res['comment_count'] = video.comment_count
        res['view_count'] = video.view_count
        count_list = []
        for analyse in analyse_list:
            count_list.append({
                'like_count': analyse.total_like_count,
                'comment_count': analyse.total_comment_count,
                'view_count': analyse.total_view_count
            })
        res['count_list'] = count_list
        return app.utils.gen_response(200, res)

    else:
        return app.utils.gen_response(405)