"""
this is a module for analyse the information of fans
"""
import app.utils
import app.times
import analyseWorks.views
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
            analyse_list = AnalyseHour.objects.filter(
                user_id=open_id).order_by('sum_time')

            res_list = analyseWorks.views.return_response(begin_timestamp, term_timestamp, analyse_list, 3600)
            res = {'count_list': res_list}
            return app.utils.gen_response(200, res)
        except:
            return app.utils.gen_response(400)
    return app.utils.gen_response(405)
