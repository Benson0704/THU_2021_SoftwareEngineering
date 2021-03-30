"""
this module provides api connected to kuaishou api to fetch data
"""

import requests


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


def get_user_data(app_id, access_token):
    """
    通过user_info接口得到用户的快手公开资料
    return: user_data
    """
    user_url = "https://open.kuaishou.com/openapi/user_info"
    params = {"access_token": access_token, "app_id": app_id}
    user_data = requests.get(url=user_url, params=params).json()
    return user_data


def get_video_data(access_token, app_id):
    """
    通过list接口得到用户的全部video_list信息
    return: video_data
    """
    url = "https://open.kuaishou.com/openapi/tsinghua/photo/list"
    params = {"access_token": access_token, "app_id": app_id}
    video_data = requests.get(url=url, params=params).json()
    return video_data


def get_count_data(access_token, app_id):
    """
    通过count接口得到用户的视频数量统计信息
    return: count_data
    """
    count_url = "https://open.kuaishou.com/openapi/photo/count"
    params = {"access_token": access_token, "app_id": app_id}
    count_data = requests.get(url=count_url, params=params).json()
    return count_data
