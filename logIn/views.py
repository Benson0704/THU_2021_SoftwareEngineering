"""
this is a module for getting the information of users
and videos in the login process
"""

import os
import requests
from django.http import JsonResponse
from logIn.utils import is_registered, update_registered_user, \
    initialize_new_user, get_total_like_count, \
    get_total_comment_count, get_total_view_count, store_token

OAUTH = {
    "app_id": "ks692991395583662522",
    "app_secret": "SQQoA2MFqcdeRF_vbFttIw",  # 需要存储在服务器端，不能暴露
    "scope": "user_info,user_video_info",
    "response_type": "code",
    "auth_url": "https://open.kuaishou.com/oauth2/authorize",
    "token_url": "https://open.kuaishou.com/oauth2/access_token",
    "redirect_uri": "http://127.0.0.1:8000/logIn/oauth/callback"
}
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'


def oauth_callback(request):
    """
    this function get the request from frontend
    return: code, data
    """

    def gen_response(code: int, data: str):
        return JsonResponse({
            'code': code,
            'data': data
        }, status=code)

    if request.method == 'GET':
        code = request.GET.get('code')
        body = {
            "app_id": OAUTH["app_id"],
            "app_secret": OAUTH["app_secret"],
            "code": code,
            "grant_type": "authorization_code"
        }
        response = requests.post(OAUTH["token_url"], body).json()
        result = response.get("result")
        if result != '1':
            return gen_response(404, response.get("error_msg"))

        access_token = response.get("access_token")
        open_id = response.get("open_id")
        refresh_token = response.get("refresh_token")
        store_token(open_id, access_token, refresh_token)

        # 通过user_info接口得到用户的快手公开资料
        user_url = "https://open.kuaishou.com/openapi/user_info"
        params = {"access_token": access_token, "app_id": OAUTH["app_id"]}
        user_data = requests.get(url=user_url, params=params).json()
        name = user_data.get("name")
        sex = user_data.get("sex")
        fan = user_data.get("fan")
        follow = user_data.get("follow")
        head = user_data.get("head")
        big_head = user_data.get("bigHead")
        city = user_data.get("city")

        # 通过list接口得到用户的全部video_list信息
        url = "https://open.kuaishou.com/openapi/tsinghua/photo/list"
        params = {"access_token": access_token, "app_id": OAUTH["app_id"]}
        video_data = requests.get(url=url, params=params).json()
        video_list = video_data.get("video_list")

        # 通过count接口得到用户的视频数量统计信息
        count_url = "https://open.kuaishou.com/openapi/photo/count"
        res = requests.get(url=count_url, params=params)
        count_data = res.json()
        all_count = count_data["all_count"]
        private_count = count_data["private_count"]
        public_count = count_data["public_count"]
        friend_count = count_data["friend_count"]

        if is_registered(open_id):
            update_registered_user(open_id, user_data, video_list, count_data)
        else:
            initialize_new_user(open_id, user_data, video_list, count_data)

        total_like_count = get_total_like_count(open_id)
        total_comment_count = get_total_comment_count(open_id)
        total_view_count = get_total_view_count(open_id)

        data = {
                'user_data': {
                    "name": name,
                    "sex": sex,
                    "fan": fan,
                    "follow": follow,
                    "head": head,
                    "bigHead": big_head,
                    "city": city
                },
                'video_data': {
                    'video_count': all_count,
                    'public_count': public_count,
                    'private_count': private_count,
                    'friend_count': friend_count,
                    'total_like_count': total_like_count,
                    'total_comment_count': total_comment_count,
                    'total_view_count': total_view_count
                }
        }
        return gen_response(200, data.__str__())

    return gen_response(405, 'method {} not allowed'.
                        format(request.method))
