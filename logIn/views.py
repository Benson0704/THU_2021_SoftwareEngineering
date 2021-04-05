"""
this is a module for getting the information
of users and videos in the login process
"""
from datetime import datetime

from django.http import JsonResponse

import app.api
import app.utils
import app.times


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
        token_data = app.api.get_token_data(code)
        result = token_data.get("result")
        if result != 1:
            return gen_response(404, token_data.get("error_msg"))

        access_token = token_data.get("access_token")
        open_id = token_data.get("open_id")
        refresh_token = token_data.get("refresh_token")

        data = app.api.get_all_data(open_id, access_token)
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

        video_change = 0
        like_change = 0
        comment_change = 0
        view_change = 0
        time = app.times.datetime2string(datetime.now())
        today_time = time.split(' ')[0] + " 00:00:00"
        today_timestamp = app.times.string2timestamp(today_time)
        yesterday_timestamp = today_timestamp - 24 * 60 * 60
        yesterday_videos = app.utils.get_videos_by_timestamp(
            open_id, yesterday_timestamp, today_timestamp)
        for video in yesterday_videos:
            video_change += 1
            like_change += video.like_count
            comment_change += video.comment_count
            view_change += video.view_change

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
            "yesterday_change": {
                "video_change": video_change,
                "like_change": like_change,
                "comment_change": comment_change,
                "view_change": view_change
            }
        }
        return gen_response(200, str(data))

    return gen_response(405, 'method {} not allowed'.
                        format(request.method))
