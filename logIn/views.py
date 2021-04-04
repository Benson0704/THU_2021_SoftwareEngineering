"""
this is a module for getting the information
of users and videos in the login process
"""

from django.http import JsonResponse

import app.api
import app.utils

OAUTH = {
    "app_id": "ks692991395583662522",
    "app_secret": "SQQoA2MFqcdeRF_vbFttIw",  # 需要存储在服务器端，不能暴露
}


def oauth_callback(request):
    """
    this function get the request from frontend
    return: code, data
    """
    if request.method == 'GET':
        code = request.GET.get('code')
        token_data = app.api.get_token_data(code, OAUTH["app_id"],
                                            OAUTH["app_secret"])
        result = token_data.get("result")
        if result != 1:
            return app.utils.gen_response(404, token_data.get("error_msg"))

        access_token = token_data.get("access_token")
        open_id = token_data.get("open_id")
        refresh_token = token_data.get("refresh_token")

        data = app.api.get_all_data(OAUTH["app_id"], OAUTH["app_secret"],
                                    open_id, access_token)
        user_data = data[0]
        name = user_data.get("name")
        sex = user_data.get("sex")
        if sex == 'F':
            sex = 1
        else:
            if sex == 'M':
                sex = 0
            else:
                sex = None
        fan = user_data.get("fan")
        follow = user_data.get("follow")
        head = user_data.get("head")
        big_head = user_data.get("bigHead")
        city = user_data.get("city")

        video_data = data[1]
        count_data = data[2]
        all_count = count_data["all_count"]
        private_count = count_data["private_count"]
        public_count = count_data["public_count"]
        friend_count = count_data["friend_count"]

        app.api.store_data(open_id, user_data,
                           video_data, count_data)
        app.utils.store_token(open_id, access_token, refresh_token)

        total_like_count = app.utils.get_total_like_count(open_id)
        total_comment_count = app.utils.get_total_comment_count(open_id)
        total_view_count = app.utils.get_total_view_count(open_id)

        yesterday_change = app.utils.get_yesterday_change(open_id)

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
            },
            "yesterday_change": yesterday_change
        }
        return app.utils.gen_response(200, data)

    return app.utils.gen_response(405, 'method {} not allowed'.
                        format(request.method))
