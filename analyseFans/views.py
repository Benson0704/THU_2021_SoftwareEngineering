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
            analyse_list = AnalyseHour.objects.filter(user_id=open_id)

            count_list = [[0 for i in range(3)] for j in range(25)]
            res_list = []
            for analyse in analyse_list:
                timestamp = app.times.datetime2timestamp(analyse.sum_time)
                if begin_timestamp <= timestamp <= term_timestamp:
                    idx = int((timestamp - begin_timestamp) / 3600)
                    count_list[idx][0] += analyse.total_like_count
                    count_list[idx][1] += analyse.total_comment_count
                    count_list[idx][2] += analyse.total_view_count

            for idx in range(1, 25):
                if count_list[idx][0] == 0 and count_list[idx][
                        1] == 0 and count_list[idx][2] == 0:
                    continue
                else:
                    res_list.append({
                        'like_count':
                        count_list[idx][0] - count_list[idx - 1][0],
                        'comment_count':
                        count_list[idx][1] - count_list[idx - 1][1],
                        'view_count':
                        count_list[idx][2] - count_list[idx - 1][2]
                    })
            res = {'count_list': res_list}
            return app.utils.gen_response(200, res)
        except Exception as exception:
            return app.utils.gen_response(400, repr(exception))
    return app.utils.gen_response(405)
