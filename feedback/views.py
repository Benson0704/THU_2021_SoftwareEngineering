"""
this is a module for getting and reply feedbacks
finished: 4.21
"""
import json
import time
import traceback
import app.utils
import app.times
from app.models import User, Message, Feedback


def operate_feedback_user(request):
    """
    this function operate feedback for user
    return: code, data
    """
    if request.method == 'GET':
        try:
            open_id = request.GET['open_id']
            user = User.objects.get(open_id=open_id)
            total_list = user.message.all().order_by('-create_time')
            unsolved_list = []
            solved_list = []
            for message in total_list:
                if message.status == 0:
                    unsolved_list.append({
                        'title':
                        message.title,
                        'content':
                        message.content,
                        'timestamp':
                        app.times.datetime2timestamp((message.create_time))
                    })
                if message.status == 1:
                    feedback = message.feedback.all()
                    solved_list.append({
                        'title':
                        message.title,
                        'content':
                        message.content,
                        'timestamp':
                        app.times.datetime2timestamp((message.create_time)),
                        'admin_name':
                        User.objects.get(open_id=feedback[0].manager).name,
                        'response':
                        feedback[0].content,
                        'response_timestamp':
                        app.times.datetime2timestamp((feedback[0].create_time))
                    })
            return app.utils.gen_response(
                200, {
                    'unsolved_feedbacks': unsolved_list,
                    'solved_feedbacks': solved_list
                })
        except Exception:
            return app.utils.gen_response(400, traceback.format_exc())
    if request.method == 'POST':
        try:
            ret = request.body
            ret = json.loads(ret.decode('utf-8'))
            new_message = Message(
                user=User.objects.get(open_id=ret['open_id']),
                create_time=app.times.timestamp2datetime(ret['timestamp']),
                content=ret['content'],
                title=ret['title'])
            new_message.save()
            return app.utils.gen_response(200)
        except Exception:
            return app.utils.gen_response(400, traceback.format_exc())
    return app.utils.gen_response(405)


def operate_feedback_admin(request):
    """
    this function operate feedback for admin
    return: code, data
    """
    if request.method == 'GET':
        try:
            messages = Message.objects.all().order_by('-create_time')
            unsolved_list = []
            solved_list = []
            for message in messages:
                if message.status == 0:
                    unsolved_list.append({
                        'user_name':
                        message.user.name,
                        'user_open_id':
                        message.user.open_id,
                        'title':
                        message.title,
                        'content':
                        message.content,
                        'timestamp':
                        app.times.datetime2timestamp(message.create_time)
                    })
                if message.status == 1:
                    feedback = message.feedback.all()
                    solved_list.append({
                        'title':
                        message.title,
                        'content':
                        message.content,
                        'admin_name':
                        User.objects.get(open_id=feedback[0].manager).name,
                        'response':
                        feedback[0].content,
                        'response_timestamp':
                        app.times.datetime2timestamp(feedback[0].create_time),
                        'timestamp':
                        app.times.datetime2timestamp((message.create_time)),
                        'user_name':
                        message.user.name,
                    })
            return app.utils.gen_response(
                200, {
                    'unsolved_feedbacks': unsolved_list,
                    'solved_feedbacks': solved_list
                })
        except Exception:
            return app.utils.gen_response(400, traceback.format_exc())
    if request.method == 'POST':
        try:
            ret = request.body
            ret = json.loads(ret.decode('utf-8'))
            message = Message.objects.get(
                user=User.objects.get(open_id=ret['user_open_id']),
                create_time=app.times.timestamp2datetime(ret['timestamp']))
            message.save()
            feedback = Feedback(user=ret['user_open_id'],
                                create_time=app.times.timestamp2datetime(
                                    time.time()),
                                message=message,
                                manager=ret['open_id'],
                                content=ret['response'])
            feedback.save()
            if message.status == 0:
                message.status = 1
                message.save()
                return app.utils.gen_response(200)
            if message.status == 1:
                return app.utils.gen_response(210)
        except Exception:
            return app.utils.gen_response(400, traceback.format_exc())
    return app.utils.gen_response(405)
