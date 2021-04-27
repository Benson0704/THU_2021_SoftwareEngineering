"""
this is a module for analyse the information of videos
"""

import app.utils
import app.times
from app.models import Video, Analyse


def get_register_time(request):
    if request.method == 'GET':
        try:
            open_id = request.GET.get('open_id')
            return app.utils.gen_response(
                200, {
                    'start_timestamp':
                    app.times.datetime2timestamp(
                        Analyse.objects.filter(
                            user_id=open_id).order_by('sum_time')[0].sum_time)
                })
        except Exception as exception:
            return app.utils.gen_response(400, str(exception))
    return app.utils.gen_response(405)


def get_videos_info_by_time(request):
    '''
    returns the videos' comment etc infos
    startpoint: the biggest timestamp < begin
    timestamp tackle method:[ , ]
    '''
    if request.method == 'GET':
        try:
            photo_id = request.GET['photo_id']
            begin_timestamp = int(request.GET['begin_timestamp'])
            term_timestamp = int(request.GET['term_timestamp'])
            video = Video.objects.get(photo_id=photo_id)
            analyse_list = (Analyse.objects.filter(
                video=video).order_by('sum_time'))
            res = {}
            res['photo_id'] = photo_id
            res['caption'] = video.caption
            res['cover'] = video.cover
            res['play_url'] = video.play_url
            res['create_time'] = app.times.datetime2timestamp(
                video.create_time)
            res['pending'] = False
            res['like_count'] = video.like_count
            res['comment_count'] = video.comment_count
            res['view_count'] = video.view_count
            count_list = []
            res_list = []
            if len(analyse_list) != 0:
                begin_timestamp = max(
                    begin_timestamp,
                    app.times.datetime2timestamp(analyse_list[0].sum_time))
            while begin_timestamp <= term_timestamp + 1:
                for analyse in analyse_list:
                    if begin_timestamp == app.times.datetime2timestamp(
                            analyse.sum_time):
                        count_list.append({
                            'like_count':
                            analyse.total_like_count,
                            'comment_count':
                            analyse.total_comment_count,
                            'view_count':
                            analyse.total_view_count
                        })
                begin_timestamp += 86400
            for i, _ in enumerate(count_list):
                if len(count_list) == 1:
                    res_list.append({
                        'like_count':
                        count_list[i]['like_count'],
                        'comment_count':
                        count_list[i]['comment_count'],
                        'view_count':
                        count_list[i]['view_count']
                    })
                    break
                if i != len(count_list) - 1:
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
        except Exception as exception:
            return app.utils.gen_response(400, str(exception))
    return app.utils.gen_response(405)


def get_all_videos_info(request):
    '''
    returns the a user's all videos' comment etc infos
    timestamp tackle method:[ , ]
    '''
    if request.method == 'GET':
        try:
            open_id = request.GET['open_id']
            begin_timestamp = int(request.GET['begin_timestamp'])
            term_timestamp = int(request.GET['term_timestamp'])
            recent_data = {
                'like_count': 0,
                'comment_count': 0,
                'view_count': 0
            }
            user = User.objects.get(open_id=open_id)
            video_list = user.video.all()
            res_list = []
            for _ in range((term_timestamp + 1 - begin_timestamp) / 86400):
                res_list.append({
                    'video_count': 0,
                    'like_count': 0,
                    'comment_count': 0,
                    'view_count': 0
                })
            for video in video_list:
                analyses = video.analysis.all().order_by('sum_time')
                for i, analyse in enumerate(analyses):
                    if begin_timestamp <= app.times.datetime2timestamp(
                            analyse.sum_time) < term_timestamp:
                        res_list[
                            (app.times.datetime2timestamp(analyse.sum_time) -
                             begin_timestamp) / 86400 -
                            1]['like_count'] += analyses[
                                i + 1].total_like_count - analyses[
                                    i].total_like_count
                        res_list[
                            (app.times.datetime2timestamp(analyse.sum_time) -
                             begin_timestamp) / 86400 -
                            1]['comment_count'] += analyses[
                                i + 1].total_comment_count - analyses[
                                    i].total_comment_count
                        res_list[
                            (app.times.datetime2timestamp(analyse.sum_time) -
                             begin_timestamp) / 86400 -
                            1]['view_count'] += analyses[
                                i + 1].total_view_count - analyses[
                                    i].total_view_count
            begin = begin_timestamp
            while begin <= term_timestamp:
                for video in video_list:
                    if begin <= app.times.datetime2timestamp(
                            video.create_time) < begin + 86400:
                        res_list[(begin - begin_timestamp) /
                                 86400]['video_count'] += 1
                begin += 86400
            return app.utils.gen_response(200, {
                'recent_data': recent_data,
                'count_list': res_list
            })
        except Exception as exception:
            return app.utils.gen_response(400, str(exception))
    return app.utils.gen_response(405)


def test(request):
    if request.method == 'GET':
        try:
            open_id = request.GET['open_id']
            user = User.objects.filter(open_id=open_id)
            video_list = user.video.all()
            res = {}
            for video in video_list:
                res[str(video.photo_id)]: []
                analyses = video.analysis.all().order_by('sum_time')
                for ana in analyses:
                    res[str(video.photo_id)].append({
                        'time':
                        app.times.datetime2timestamp(ana.sum_time),
                        'view':
                        ana.total_view_count,
                        'comment':
                        ana.total_comment_count,
                        'like':
                        ana.total_like_count
                    })
            return app.utils.gen_response(200, res)
        except Exception as exception:
            return app.utils.gen_response(400, str(exception))
    else:
        return app.utils.gen_response(405)