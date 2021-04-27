"""
this is a module for getting the information shared users
"""
import json
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
            sharer_user = User.objects.get(open_id=sharer_openid)
            sharer_user.auth_user += shared_openid + '_&_'
            sharer_user.save()
            shared_user = User.objects.get(open_id=shared_openid)
            shared_user.authed_user += sharer_openid + '_&_'
            shared_user.save()
            return app.utils.gen_response(200)
        except Exception as exception:
            return app.utils.gen_response(400, repr(exception))
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
            sharer_user.auth_user.replace(shared_openid + '_&_', '')
            sharer_user.save()
            shared_user = User.objects.get(open_id=shared_openid)
            shared_user.authed_user.replace(sharer_openid + '_&_', '')
            shared_user.save()
            return app.utils.gen_response(200)
        except Exception as exception:
            return app.utils.gen_response(400, repr(exception))
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
                    user = User.objects.get(open_id=ids)
                    res_list.append({
                        'open_id': ids,
                        'name': user.name,
                        'head': user.head
                    })
            return app.utils.gen_response(200, {'sharing_list': res_list})
        except Exception as exception:
            return app.utils.gen_response(400, repr(exception))
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
                    user = User.objects.get(open_id=ids)
                    res_list.append({
                        'open_id': ids,
                        'name': user.name,
                        'head': user.head
                    })
            return app.utils.gen_response(200, {'shared_list': res_list})
        except Exception as exception:
            return app.utils.gen_response(400, repr(exception))
    return app.utils.gen_response(405)


def get_user_by_name(request):
    if request.method == 'GET':
        try:
            exp_name = request.GET.get('exp_name')
            user_list = User.objects.filter(name=exp_name)
            res_list = []
            for user in user_list:
                res_list.append({
                    'open_id': user.open_id,
                    'name': user.name,
                    'head': user.head,
                    'city': user.city,
                    'fan': user.fan,
                    'video_count': user.video_count
                })
            return app.utils.gen_response(200, res_list)
        except Exception as exception:
            return app.utils.gen_response(400, repr(exception))
    return app.utils.gen_response(405)
