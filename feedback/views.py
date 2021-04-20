"""
this is a module for getting and reply feedbacks
"""
import json
import app.utils
import app.times


def operate_feedback_user(request):
    """
    this function operate feedback for user
    return: code, data
    """
    if request.method == 'GET':
        try:
            pass
        except:
            return app.utils.gen_response(400)
    if request.method == 'POST':
        try:
            ret = request.body
            ret = json.loads(ret.decode('utf-8'))
        except:
            return app.utils.gen_response(400)
    return app.utils.gen_response(405)


def operate_feedback_admin(request):
    """
    this function operate feedback for admin
    return: code, data
    """
    if request.method == 'GET':
        try:
            pass
        except:
            return app.utils.gen_response(400)
    if request.method == 'POST':
        try:
            ret = request.body
            ret = json.loads(ret.decode('utf-8'))
        except:
            return app.utils.gen_response(400)
    return app.utils.gen_response(405)
