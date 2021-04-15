"""
this is a module for analyse the information of videos
"""

import app.utils
import app.times
from app.models import User, Video, Analyse


def get_videos_info_by_time(request):
    '''
    returns the videos' comment etc infos
    startpoint: the biggest timestamp < begin
    timestamp tackle method:[ , ]
    '''
    if request.method == 'GET':
        try:
            photo_id = request.GET.get('photo_id')
            begin_timestamp = int(request.GET.get('begin_timestamp'))
            term_timestamp = int(request.GET.get('term_timestamp'))
            video = Video.objects.get(photo_id=photo_id)
            analyse_list = []
            analyse_list = (Analyse.objects.filter(video=video)
                            .order_by('sum_time'))
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
            res_list = []
            for analyse in analyse_list:
                if begin_timestamp == app.times.datetime2timestamp(
                        analyse.sum_time) + 1:
                    count_list.append({
                        'like_count': analyse.total_like_count,
                        'comment_count': analyse.total_comment_count,
                        'view_count': analyse.total_view_count
                    })
                if begin_timestamp <= app.times.datetime2timestamp(
                        analyse.sum_time) <= term_timestamp:
                    count_list.append({
                        'like_count': analyse.total_like_count,
                        'comment_count': analyse.total_comment_count,
                        'view_count': analyse.total_view_count
                    })
            for i, dic in enumerate(count_list):
                if dic != count_list[-1]:
                    res_list.append({
                        'like_count':
                        count_list[i + 1]['like_count'] -
                        count_list[i]['like_count'],
                        'comment_count':
                        count_list[i + 1]['comment_count'] -
                        count_list[i]['comment_count'],
                        'view_count':
                        count_list[i + 1]['view_count'] -
                        count_list[i]['view_count']
                    })
            res['count_list'] = res_list
            return app.utils.gen_response(200, res)
        except:
            return app.utils.gen_response(400)
    return app.utils.gen_response(405)


def get_all_videos_info(request):
    '''
    returns the a user's all videos' comment etc infos
    timestamp tackle method:[ , ]
    '''
    if request.method == 'GET':
        try:
            open_id = request.GET.get('open_id')
            begin_timestamp = int(request.GET.get('begin_timestamp'))
            term_timestamp = int(request.GET.get('term_timestamp'))
            recent_data = {'like_count': 0, 'comment_count': 0,
                           'view_count': 0}
            analyse_list = Analyse.objects.filter(
                user_id=open_id).order_by('-sum_time')
            for analyse in analyse_list:
                if(app.times.datetime2timestamp(analyse.sum_time) +
                   86400 * 3 == term_timestamp):
                    recent_data['like_count'] += analyse.total_like_count
                    recent_data['comment_count'] += analyse.total_comment_count
                    recent_data['view_count'] += analyse.total_view_count
            recent_data['like_count'] = app.utils.get_total_like_count(
                open_id) - recent_data['like_count']
            recent_data['comment_count'] = app.utils.get_total_comment_count(
                open_id) - recent_data['comment_count']
            recent_data['view_count'] = app.utils.get_total_view_count(
                open_id) - recent_data['view_count']
            count_list = []
            res_list = []
            analyse_list = Analyse.objects.filter(
                user_id=open_id).order_by('sum_time')
            begin_timestamp -= 1
            for analyse in analyse_list:
                if begin_timestamp == app.times.datetime2timestamp(
                        analyse.sum_time):
                    count_list.append({
                        'like_count': 0,
                        'comment_count': 0,
                        'view_count': 0
                    })
                    count_list[-1]['like_count'] += analyse.total_like_count
                    count_list[-1]['comment_count'] += \
                        analyse.total_comment_count
                    count_list[-1]['view_count'] += analyse.total_view_count
                    begin_timestamp += 86400
                    if(begin_timestamp > term_timestamp):
                        break
            for i, dic in enumerate(count_list):
                if dic != count_list[-1]:
                    res_list.append({
                        'like_count':
                        count_list[i + 1]['like_count'] -
                        count_list[i]['like_count'],
                        'comment_count':
                        count_list[i + 1]['comment_count'] -
                        count_list[i]['comment_count'],
                        'view_count':
                        count_list[i + 1]['view_count'] -
                        count_list[i]['view_count']
                    })
            return app.utils.gen_response(200, {
                'recent_data': recent_data,
                'count_list': res_list
            })
        except:
            return app.utils.gen_response(400)
    return app.utils.gen_response(405)
