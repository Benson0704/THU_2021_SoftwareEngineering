"""
this is a module for getting notice information
for user and admin
"""
import json
import app.utils
import app.times
from app.models import Notice


def get_notice_user(request):
    """
    this function get notice for users
    return: code, data
    """
    if request.method == 'GET':
        try:
            open_id = request.GET['open_id']
            notices = Notice.objects.all().order_by('-create_time')
            notice_list = []
            for notice in notices:
                notice_list.append({
                    'title':
                        notice.title,
                    'content':
                        notice.content,
                    'timestamp':
                        app.times.datetime2timestamp(notice.create_time)
                })
            flow_list = app.utils.get_flow(open_id)
            print(flow_list)
            print(notice_list)
            return app.utils.gen_response(
                200, {'data': {
                    'notices': notice_list,
                    'flows': flow_list
                }})
        except:
            return app.utils.gen_response(400)
    return app.utils.gen_response(405)


def operate_notice_admin(request):
    """
    this function operate notice for admins
    return: code, data
    """
    if request.method == 'GET':
        try:
            notices = Notice.objects.all().order_by('-create_time')
            notice_list = []
            for notice in notices:
                notice_list.append({
                    'title':
                        notice.title,
                    'content':
                        notice.content,
                    'timestamp':
                        app.times.datetime2timestamp(notice.create_time)
                })
            return app.utils.gen_response(200,
                                          {'data': {
                                              'notices': notice_list
                                          }})
        except:
            return app.utils.gen_response(400)
        return app.utils.gen_response(405)
    if request.method == 'POST':
        try:
            ret = request.body
            ret = json.loads(ret.decode('utf-8'))
            new_notice = Notice(
                create_time=app.times.timestamp2datetime(ret['timestamp']),
                content=ret['content'],
                title=ret['title'],
                publish_user=ret['open_id'])
            new_notice.save()
            return app.utils.gen_response(200)
        except:
            return app.utils.gen_response(400)
    return app.utils.gen_response(405)
