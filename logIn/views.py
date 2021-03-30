'''
this is a module for getting the information
of users and videos in the login process
'''

import os
from django.http import JsonResponse

import app.api
import logIn.utils

OAUTH = {
    "app_id": "ks692991395583662522",
    "app_secret": "SQQoA2MFqcdeRF_vbFttIw",  # 需要存储在服务器端，不能暴露
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
        token_data = app.api.get_token_data(code, OAUTH["app_id"], OAUTH["app_secret"])
        result = token_data.get("result")
        if result != '1':
            return gen_response(404, token_data.get("error_msg"))

        access_token = token_data.get("access_token")
        open_id = token_data.get("open_id")
        refresh_token = token_data.get("refresh_token")
        logIn.utils.store_token(open_id, access_token, refresh_token)

        user_data = app.api.get_user_data(OAUTH["app_id"], access_token)
        name = user_data.get("name")
        sex = user_data.get("sex")
        fan = user_data.get("fan")
        follow = user_data.get("follow")
        head = user_data.get("head")
        big_head = user_data.get("bigHead")
        city = user_data.get("city")

        video_data = app.api.get_video_data(access_token, OAUTH["app_id"])
        video_list = video_data.get("video_list")

        count_data = app.api.get_count_data(access_token, OAUTH["app_id"])
        all_count = count_data["all_count"]
        private_count = count_data["private_count"]
        public_count = count_data["public_count"]
        friend_count = count_data["friend_count"]

        if logIn.utils.is_registered(open_id):
            logIn.utils.update_registered_user(open_id, user_data, video_list, count_data)
        else:
            logIn.utils.initialize_new_user(open_id, user_data, video_list, count_data)

        total_like_count = logIn.utils.get_total_like_count(open_id)
        total_comment_count = logIn.utils.get_total_comment_count(open_id)
        total_view_count = logIn.utils.get_total_view_count(open_id)

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
