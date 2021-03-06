"""
this is a module for getting the information
of users and videos in the login process
"""
import traceback
from datetime import datetime
from django.http import HttpResponse
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, \
    register_job, register_events
import app.api
import app.utils
import app.times
from app.models import User, Performance, Request


try:
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), "default")

    @register_job(scheduler,
                  'cron',
                  day_of_week='mon-sun',
                  hour='0-23',
                  id='hourly_task',
                  misfire_grace_time=3600,
                  replace_existing=True)
    def hourly_fetch_data():
        """
        this function is supposed to run in hourly period
        to fetch data and store data from api
        also add flow alarm for the notice module
        """
        for open_id in app.utils.get_all_open_id():
            access_token = app.utils.get_token(open_id)[0]
            data = app.api.get_all_data(open_id, access_token)
            app.api.manage_data(open_id)
            app.api.store_data(open_id, data[0], data[1], data[2])
            now_time = app.times.datetime2string(datetime.now())
            time = now_time.split(':')[0] + ":00:00"
            app.utils.analyse_hour_data(open_id, data[1], time)
            now_timestamp = app.times.string2timestamp(time)
            one_hour_before_time = now_timestamp - 60 * 60
            one_day_before_time = now_timestamp - 24 * 60 * 60
            app.utils.store_flow(open_id, one_day_before_time,
                                 one_hour_before_time, now_timestamp)
            qps_dict = {}
            time_cost_dict = {}
            for request in Request.objects.all():
                timestamp = app.times.datetime2timestamp(request.create_time)
                if now_timestamp - 3600 <= timestamp <= now_timestamp:
                    if request.request_type not in qps_dict:
                        qps_dict[request.request_type] = [0] * 3600
                    qps_dict[request.request_type][int(timestamp -
                                                       now_timestamp +
                                                       3600)] += 1
                if request.request_type not in time_cost_dict:
                    time_cost_dict[request.request_type] = []
                time_cost_dict[request.request_type].append(request.timecost)
            for request_type in iter(time_cost_dict):
                time_list = sorted(time_cost_dict[request_type])
                idx = len(time_list) * 99 // 100
                if idx == 0:
                    idx = 1
                P99 = time_list[idx - 1]
                if request_type in qps_dict:
                    max_qps = max(qps_dict[request_type])
                else:
                    max_qps = 0
                found = False
                for performance in Performance.objects.all():
                    if performance.api == request_type:
                        performance.P99 = P99
                        performance.qps = max(performance.qps, max_qps)
                        found = True
                        performance.save()
                        break
                if not found:
                    data = Performance.objects.create(api=request_type,
                                                      P99=P99,
                                                      qps=max_qps)
                    data.save()

    @register_job(scheduler,
                  'cron',
                  day_of_week='mon-sun',
                  hour='16',
                  id='daily_task',
                  replace_existing=True)
    def daily_fetch_data():
        """
        this function is supposed to run in daily period
        to fetch data and store data from api
        """
        for open_id in app.utils.get_all_open_id():
            access_token = app.utils.get_token(open_id)[0]
            data = app.api.get_all_data(open_id, access_token)
            app.api.manage_data(open_id)
            app.api.store_data(open_id, data[0], data[1], data[2])
            now_time = app.times.datetime2string(datetime.now())
            time = now_time.split(':')[0] + ":00:00"
            app.utils.analyse_daily_data(open_id, data[1], time)

    register_events(scheduler)
    scheduler.start()
except Exception:
    print(traceback.format_exc())
# scheduler.shutdown()


def get_yesterday_change(open_id):
    """
    this function is used by the get_user_info_by_code
     and get_user_info_by_id function to generate data
    """
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
        view_change += video.view_count
    yesterday_change = {
        "video_change": video_change,
        "like_change": like_change,
        "comment_change": comment_change,
        "view_change": view_change
    }
    return yesterday_change


def get_user_info_by_code(request):
    """
    this function get the request from frontend
    return: code, data
    """
    if request.method == 'GET':
        code = request.GET.get('code')
        token_data = app.api.get_token_data(code)
        result = token_data.get("result")
        if result != 1:
            return app.utils.gen_response(404, token_data.get("error_msg"))

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

        app.api.store_data(open_id, user_data, video_data, count_data)
        app.utils.store_token(open_id, access_token, refresh_token)

        total_like_count = app.utils.get_total_like_count(open_id)
        total_comment_count = app.utils.get_total_comment_count(open_id)
        total_view_count = app.utils.get_total_view_count(open_id)
        if app.utils.is_administrator(open_id):
            admin = 1
        else:
            admin = 0
        data = {
            'user_data': {
                'admin': admin,
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
            "yesterday_change": get_yesterday_change(open_id),
            'open_id': open_id
        }
        return app.utils.gen_response(200, data)

    return app.utils.gen_response(405, 'no such method')


def get_user_info_by_id(request):
    """
    this function get the user info for frontend
    return: userdata, videodata, open_id
    """
    if request.method == 'GET':
        open_id = request.GET.get('open_id')
        _, user_info = app.utils.get_registered_user(open_id)
        return app.utils.gen_response(
            200, {
                'user_data': {
                    'name': user_info['name'],
                    'fan': user_info['fan'],
                    'follow': user_info['follow'],
                    'head': user_info['head'],
                    'bigHead': user_info['bigHead'],
                    'city': user_info['city']
                },
                'video_data': {
                    'video_count':
                    user_info['video_count'],
                    'public_count':
                    user_info['public_count'],
                    'friend_count':
                    user_info['friend_count'],
                    'private_count':
                    user_info['private_count'],
                    'total_like_count':
                    app.utils.get_total_like_count(open_id),
                    'total_comment_count':
                    app.utils.get_total_comment_count(open_id),
                    'total_view_count':
                    app.utils.get_total_view_count(open_id)
                },
                "yesterday_change": get_yesterday_change(open_id),
                'open_id': open_id
            })
    return app.utils.gen_response(405)


def add_test(request):
    """
    this is for test add function
    """
    if request.method == 'GET':
        print("hello")
        User.objects.filter(open_id="hello").delete()
        user = User.objects.create(open_id="hello", name="??????")
        user.save()
    return HttpResponse("hello")


def delete_test(request):
    """
    this is for test delete function
    """
    if request.method == 'GET':
        User.objects.filter(open_id="hello").delete()
    return HttpResponse("hello")
