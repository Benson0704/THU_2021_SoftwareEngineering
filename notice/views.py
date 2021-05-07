"""
this is a module for getting notice information
for user and admin
"""
import json
import traceback
import app.utils
import app.times
from app.models import Notice, User


def get_notice_user(request):
    """
    this function get notice for users
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
            return app.utils.gen_response(200, {
                'notices': notice_list
            })
        except Exception:
            return app.utils.gen_response(400, traceback.format_exc())
    return app.utils.gen_response(405)


def operate_notice_admin(request):
    """
    this function operate notice for admins
    return: code, data
    """
    if request.method == 'GET':
        try:
            open_id = request.GET['open_id']
            notices = Notice.objects.all().order_by('-create_time')
            my_notices = []
            other_notices = []
            for notice in notices:
                if notice.publish_user == open_id:
                    my_notices.append({
                        'title':
                        notice.title,
                        'content':
                        notice.content,
                        'timestamp':
                        app.times.datetime2timestamp(notice.create_time)
                    })
                else:
                    other_notices.append({
                        'title':
                        notice.title,
                        'content':
                        notice.content,
                        'timestamp':
                        app.times.datetime2timestamp(notice.create_time),
                        'admin_open_id':
                        notice.publish_user,
                        'admin_name':
                        User.objects.get(open_id=notice.publish_user).name
                    })
            return app.utils.gen_response(200, {
                'my_notices': my_notices,
                'other_notices': other_notices
            })
        except Exception:
            return app.utils.gen_response(400, traceback.format_exc())
    if request.method == 'POST':
        try:
            ret = request.body
            ret = json.loads(ret.decode('utf-8'))
            if int(ret['add']) == 1:
                new_notice = Notice(create_time=app.times.timestamp2datetime(
                    ret['timestamp']),
                                    content=ret['content'],
                                    title=ret['title'],
                                    publish_user=ret['open_id'])
                new_notice.save()
            if int(ret['add']) == 0:
                old_notice = Notice.objects.filter(
                    create_time=app.times.timestamp2datetime(ret['timestamp']),
                    content=ret['content'],
                    title=ret['title'],
                    publish_user=ret['open_id'])
                old_notice.delete()
            return app.utils.gen_response(200)
        except Exception:
            return app.utils.gen_response(400, traceback.format_exc())
    return app.utils.gen_response(405)


def get_flows(request):
    """
    this function get flows for users
    return: code, data
    """
    if request.method == 'GET':
        try:
            open_id = request.GET['open_id']
            flow_list = app.utils.get_flow(open_id)
            limit = app.utils.get_limit(open_id)
            return app.utils.gen_response(200, {
                'flows': flow_list,
                'limit': limit
            })
        except Exception:
            return app.utils.gen_response(400, traceback.format_exc())
    elif request.method == 'POST':
        try:
            ret = request.body
            ret = json.loads(ret.decode('utf-8'))
            open_id = ret['open_id']
            limit = ret['limit']
            app.utils.update_limit(open_id, limit)
            return app.utils.gen_response(200)
        except Exception:
            return app.utils.gen_response(400, traceback.format_exc())
    return app.utils.gen_response(405)
