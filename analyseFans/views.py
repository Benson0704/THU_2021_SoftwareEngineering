"""
this is a module for analyse the information of fans
"""
import app.utils
import app.times
from app.models import AnalyseHour


def get_fans_info(request):
    '''
    returns the a user's all videos' comment etc infos
    timestamp tackle method:[ , ]
    '''
    if request.method == 'GET':
        try:
            open_id = request.GET['open_id']
            begin_timestamp = int(request.GET['begin_timestamp'])
            term_timestamp = int(request.GET['term_timestamp'])
            count_list = []
            res_list = []
            res = {}
            analyse_list = AnalyseHour.objects.filter(
                user_id=open_id).order_by('sum_time')
            for analyse in analyse_list:
                if begin_timestamp == app.times.datetime2timestamp(
                        analyse.sum_time):
                    count_list.append({
                        'like_count': 0,
                        'comment_count': 0,
                        'view_count': 0
                    })
                    count_list[-1]['like_count'] += analyse.total_like_count
                    count_list[-1][
                        'comment_count'] += analyse.total_comment_count
                    count_list[-1]['view_count'] += analyse.total_view_count
                begin_timestamp += 3600
                if begin_timestamp > term_timestamp:
                    break
            for i, dic in enumerate(count_list):
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