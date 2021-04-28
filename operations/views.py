import traceback
import app.utils
from app.models import User, Analyse, Video


def operate_user(request):
    if request.method == 'GET':
        try:
            open_id = request.GET.get('open_id')
            name = request.GET.get('name')
            head = 'https://tx2.a.yximgs.com/uhead/AB/2021/03/19/13/BMjAyMTAzMTkxMzU0MjRfMjMxMTc1MzAzNV8xX2hkMzEwXzk4OQ==_s.jpg'
            if int(request.GET.get('add')) == 1:
                user = User(open_id=open_id,
                            name=name,
                            head=head,
                            bigHead=head,
                            city='beijing',
                            sex=1,
                            access_token='access_token',
                            refresh_token='refresh_token')
                user.save()
            else:
                User.objects.get(open_id=open_id, name=name).delete()
            res = []
            users = User.objects.all()
            for u in users:
                res.append({
                    'open_id': u.open_id,
                    'name': u.name,
                    'admin': u.identity
                })
            return app.utils.gen_response(100, res)
        except Exception:
            return app.utils.gen_response(400, traceback.format_exc())
    return app.utils.gen_response(405)


def set_admin(request):
    if request.method == 'GET':
        try:
            open_id = request.GET.get('open_id')
            user = User.objects.get(open_id=open_id)
            user.identity = int(request.GET.get('add'))
            user.save()
            res = []
            users = User.objects.all()
            for u in users:
                res.append({
                    'open_id': u.open_id,
                    'name': u.name,
                    'admin': u.identity
                })
            return app.utils.gen_response(100, res)
        except Exception:
            return app.utils.gen_response(400, traceback.format_exc())
    return app.utils.gen_response(405)


def user_analysis(request):
    if request.method == 'GET':
        try:
            open_id = request.GET.get('open_id')
            a_list = Analyse.objects.filter(
                user_id=open_id).order_by('sum_time')
            res = []
            for i in a_list:
                res.append({
                    'video': i.video.photo_id,
                    'like': i.total_like_count,
                    'comment': i.total_comment_count,
                    'view': i.total_view_count,
                    'time': i.sum_time
                })
            return app.utils.gen_response(100, res)
        except Exception:
            return app.utils.gen_response(400, traceback.format_exc())
    return app.utils.gen_response(405)


def video_analysis(request):
    if request.method == 'GET':
        try:
            photo_id = request.GET.get('photo_id')
            video = Video.objects.get(photo_id=photo_id)
            a_list = video.analysis.all().order_by('sum_time')
            res = []
            for i in a_list:
                res.append({
                    'video': i.video.photo_id,
                    'like': i.total_like_count,
                    'comment': i.total_comment_count,
                    'view': i.total_view_count,
                    'time': i.sum_time
                })
            return app.utils.gen_response(100, res)
        except Exception:
            return app.utils.gen_response(400, traceback.format_exc())
    return app.utils.gen_response(405)
