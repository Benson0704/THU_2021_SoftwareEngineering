"""
this is a module for getting the information shared users
"""
import json
import re
import traceback
import app.utils
import app.times
from app.models import User


def add_share(request):
    '''
    receiver a sharer and a shared id
    return 200
    '''
    if request.method == 'POST':
        try:
            ret = request.body
            ret = json.loads(ret.decode('utf-8'))
            sharer_openid = ret['sharer_open_id']
            shared_openid = ret['shared_open_id']
            timestamp = ret['timestamp']
            sharer_user = User.objects.get(open_id=sharer_openid)
            sharer_user.auth_user += shared_openid + '&' + str(
                timestamp) + '_&_'
            sharer_user.save()
            shared_user = User.objects.get(open_id=shared_openid)
            shared_user.authed_user += sharer_openid + '&' + str(
                timestamp) + '_&_'
            shared_user.save()
            return app.utils.gen_response(200)
        except Exception:
            return app.utils.gen_response(400, traceback.format_exc())
    return app.utils.gen_response(405)


def delete_share(request):
    '''
    receiver a sharer and a shared id
    return 200
    '''
    if request.method == 'POST':
        try:
            ret = request.body
            ret = json.loads(ret.decode('utf-8'))
            sharer_openid = ret['sharer_open_id']
            shared_openid = ret['shared_open_id']
            sharer_user = User.objects.get(open_id=sharer_openid)
            sharer_user.auth_user = str(
                re.sub(shared_openid + r'&[0-9]+_&_', '',
                       sharer_user.auth_user))
            sharer_user.save()
            shared_user = User.objects.get(open_id=shared_openid)
            shared_user.authed_user = str(
                re.sub(sharer_openid + r'&[0-9]+_&_', '',
                       shared_user.auth_user))
            shared_user.save()
            return app.utils.gen_response(200)
        except Exception:
            return app.utils.gen_response(400, traceback.format_exc())
    return app.utils.gen_response(405)


def get_my_sharing_user(request):
    """
    this function return the user' sharing user
    return: code, data
    """
    if request.method == 'GET':
        try:
            open_id = request.GET['open_id']
            user = User.objects.get(open_id=open_id)
            if user.auth_user == '':
                return app.utils.gen_response(200, {'sharing_list': []})
            id_list = user.auth_user.split('_&_')
            res_list = []
            for ids in id_list:
                if ids != '':
                    user = User.objects.get(open_id=ids.split('&')[0])
                    res_list.append({
                        'open_id': ids.split('&')[0],
                        'name': user.name,
                        'head': user.head,
                        'timestamp': ids.split('&')[1]
                    })
            return app.utils.gen_response(200, {'sharing_list': res_list})
        except Exception:
            return app.utils.gen_response(400, traceback.format_exc())
    return app.utils.gen_response(405)


def get_user_share_to_me(request):
    """
    this function operate the shared users
    return: code, data
    """
    if request.method == 'GET':
        try:
            open_id = request.GET.get('open_id')
            user = User.objects.get(open_id=open_id)
            if user.authed_user == '':
                return app.utils.gen_response(200, {'shared_list': []})
            id_list = user.authed_user.split('_&_')
            res_list = []
            for ids in id_list:
                if ids != '':
                    user = User.objects.get(open_id=ids.split('&')[0])
                    res_list.append({
                        'open_id': ids.split('&')[0],
                        'name': user.name,
                        'head': user.head,
                        'timestamp': ids.split('&')[1]
                    })
            return app.utils.gen_response(200, {'shared_list': res_list})
        except Exception:
            return app.utils.gen_response(400, traceback.format_exc())
    return app.utils.gen_response(405)


def get_user_by_name(request):
    '''
    get all users according to names
    '''
    if request.method == 'GET':
        try:
            open_id = request.GET.get('open_id')
            me = User.objects.get(open_id=open_id)
            exp_name = request.GET.get('exp_name')
            user_list = User.objects.filter(name__contains=exp_name)
            res_list = []
            for user in user_list:
                my_auth_user = me.auth_user.split('_&_')
                my_authed_user = me.authed_user.split('_&_')
                for i, auth_user in enumerate(my_auth_user):
                    my_auth_user[i] = auth_user.split('&')[0]
                for i, authed_user in enumerate(my_authed_user):
                    my_authed_user[i] = authed_user.split('&')[0]
                if user.open_id in my_auth_user + my_authed_user:
                    continue
                res_list.append({
                    'open_id': user.open_id,
                    'name': user.name,
                    'head': user.head,
                    'city': user.city,
                    'fan': user.fan,
                    'video_count': user.video_count
                })
            return app.utils.gen_response(200, {'exp_list': res_list})
        except Exception:
            return app.utils.gen_response(400, traceback.format_exc())
    return app.utils.gen_response(405)
