"""
this module provides api connected to kuaishou api to fetch data
"""

import requests
import app.utils


def get_token_data(code, app_id, app_secret):
    """
    通过token_url接口得到token相关data
    return: token_data
    """
    body = {
        "app_id": app_id,
        "app_secret": app_secret,
        "code": code,
        "grant_type": "authorization_code"
    }
    token_url = "https://open.kuaishou.com/oauth2/access_token"
    token_data = requests.post(token_url, body).json()
    return token_data


def get_data(app_id, app_secret, open_id, url, access_token):
    """
    本函数接口可以从快手api获得url对应的用户data信息
    并且在access_token失效时尝试置换得到新的access_token
    return: url对应的data
    """
    params = {"access_token": access_token, "app_id": app_id}
    data = requests.get(url=url, params=params).json()
    if data.get("result") != '1':
        access_token = refresh_access_token(open_id, app_id, app_secret)
        params = {"access_token": access_token, "app_id": app_id}
        data = requests.get(url=url, params=params).json()
    return data


def refresh_access_token(open_id, app_id, app_secret):
    """
    通过refresh_token接口得到新的access_token
    （也可能refresh_token已过期，此时需要用户登陆时重新授权）
    return: access_token
    """
    refresh_token = app.utils.get_token(open_id)[1]
    body = {
        "app_id": app_id,
        "app_secret": app_secret,
        "refresh_token": refresh_token,
        "grant_type": "refresh_token"
    }
    token_url = "https://open.kuaishou.com/oauth2/refresh_token"
    token_data = requests.post(token_url, body).json()
    if token_data.get("result") == '1':
        app.utils.store_token(open_id, token_data.get("access_token"),
                              token_data.get("refresh_token"))
        return token_data.get("access_token")
    else:
        return "Token is not available."


def get_all_data(app_id, app_secret, open_id, access_token):
    """
    通过调用快手3个api接口分别获得user, video, count信息
    return: user_data, video_list, count_data
    """
    user_url = "https://open.kuaishou.com/openapi/user_info"
    video_url = "https://open.kuaishou.com/openapi/tsinghua/photo/list"
    count_url = "https://open.kuaishou.com/openapi/photo/count"
    user_data = get_data(app_id, app_secret, open_id, user_url, access_token)
    video_data = get_data(app_id, app_secret, open_id, video_url, access_token)
    count_data = get_data(app_id, app_secret, open_id, count_url, access_token)
    return user_data, video_data, count_data


def store_data(open_id, user_data, video_data, count_data):
    """
    判断用户是否注册过，然后将用户数据初始化/更新
    """
    registered_state = app.utils.is_registered(open_id)
    video_list = video_data["video_list"]
    if registered_state:
        app.utils.update_registered_user(open_id, user_data,
                                         video_list, count_data)
    else:
        app.utils.initialize_new_user(open_id, user_data,
                                      video_list, count_data)


def manage_data(app_id, app_secret, open_id):
    """
    本函数接口拟用于定期更新数据的任务：先获取再存储
    """
    access_token = app.utils.get_token(open_id)[0]
    data = get_all_data(app_id, app_secret, open_id, access_token)
    store_data(open_id, data[0], data[1], data[2])
