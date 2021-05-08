import traceback
import app.utils
import app.times
from app.models import User, Analyse, Video, Label


def make_fake_analysis(open_id):
    try:
        maked = 0
        user = User.objects.get(open_id=open_id)
        videos = user.video.all()
        for video in videos:
            analyses = video.analysis.all().order_by('sum_time')
            for i, analyse in enumerate(analyses):
                if i == len(analyses) - 1:
                    continue
                if app.times.datetime2timestamp(
                        analyse.sum_time
                ) + 86400 == app.times.datetime2timestamp(
                        analyses[i + 1].sum_time):
                    if analyse.total_like_count <= analyses[
                            i +
                            1].total_like_count and analyse.total_view_count <= analyses[
                                i +
                                1].total_view_count and analyse.total_comment_count <= analyses[
                                    i + 1].total_comment_count:
                        continue
                analyseHours = video.analysisHour.all().order_by('sum_time')
                for i, analyseHour in enumerate(analyseHours):
                    if app.times.datetime2timestamp(
                            analyseHour.sum_time
                    ) <= app.times.datetime2timestamp(
                            analyse.sum_time
                    ) + 86400 <= app.times.datetime2timestamp(
                            analyseHours[i + 1].sum_time):
                        new_time = app.times.timestamp2datetime(
                            app.times.datetime2timestamp(analyse.sum_time) +
                            86400)
                        old_analyse = Analyse.objects.get(sum_time=new_time,
                                                          video=video)
                        old_analyse.delete()
                        new_analyse = Analyse(
                            total_like_count=analyseHour.total_like_count,
                            total_view_count=analyseHour.total_view_count,
                            total_comment_count=analyseHour.
                            total_comment_count,
                            video=analyseHour.video,
                            user_id=open_id,
                            sum_time=new_time)
                        new_analyse.save()
                        maked = 1
                        break
        if maked == 1:
            return 'make faked'
        else:
            return 'no need'
    except:
        return traceback.format_exc()


def operate_user(request):
    if request.method == 'GET':
        try:
            head = 'https://tx2.a.yximgs.com/uhead/AB/2021/03/19/13/BMjAyMTAzMTkxMzU0MjRfMjMxMTc1MzAzNV8xX2hkMzEwXzk4OQ==_s.jpg'
            if int(request.GET.get('add')) == 1:
                open_id = request.GET.get('open_id')
                name = request.GET.get('name')
                user = User(open_id=open_id,
                            name=name,
                            head=head,
                            bigHead=head,
                            city='beijing',
                            sex=1,
                            access_token='access_token',
                            refresh_token='refresh_token')
                user.save()
            elif int(request.GET.get('add')) == 0:
                open_id = request.GET.get('open_id')
                name = request.GET.get('name')
                User.objects.get(open_id=open_id, name=name).delete()
            else:
                pass
            res = []
            users = User.objects.all()
            for u in users:
                videos = u.video.all()
                v_list = []
                for v in videos:
                    v_list.append({
                        'time':
                        app.times.datetime2string(v.create_time),
                        'photo_id':
                        v.photo_id,
                        'caption':
                        v.caption
                    })
                res.append({
                    'open_id': u.open_id,
                    'name': u.name,
                    'admin': u.identity,
                    'user can see me': u.auth_user,
                    'user i can see': u.authed_user,
                    'videos': v_list
                })
            if int(request.GET.get('add')) == 404:
                open_id = request.GET.get('open_id')
                return app.utils.gen_response(
                    200, {
                        'fake status': make_fake_analysis(open_id),
                        'info': res
                    })
            return app.utils.gen_response(200, res)
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
                videos = u.video.all()
                v_list = []
                for v in videos:
                    v_list.append({
                        'time':
                        app.times.datetime2string(v.create_time),
                        'photo_id':
                        v.photo_id,
                        'caption':
                        v.caption
                    })
                res.append({
                    'open_id': u.open_id,
                    'name': u.name,
                    'admin': u.identity,
                    'user can see me': u.auth_user,
                    'user i can see': u.authed_user,
                    'videos': v_list
                })
            return app.utils.gen_response(200, res)
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
                    'time': app.times.datetime2timestamp(i.sum_time),
                    'real time': app.times.datetime2string(i.sum_time)
                })
            return app.utils.gen_response(200, res)
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
                    'time': app.times.datetime2timestamp(i.sum_time),
                    'real time': app.times.datetime2string(i.sum_time)
                })
            return app.utils.gen_response(200, res)
        except Exception:
            return app.utils.gen_response(400, traceback.format_exc())
    return app.utils.gen_response(405)


def video_analysis_hour(request):
    if request.method == 'GET':
        try:
            photo_id = request.GET.get('photo_id')
            video = Video.objects.get(photo_id=photo_id)
            ah_list = video.analysisHour.all().order_by('sum_time')
            res = []
            for i in ah_list:
                res.append({
                    'video': i.video.photo_id,
                    'like': i.total_like_count,
                    'comment': i.total_comment_count,
                    'view': i.total_view_count,
                    'time': app.times.datetime2timestamp(i.sum_time),
                    'real time': app.times.datetime2string(i.sum_time)
                })
            return app.utils.gen_response(200, res)
        except Exception:
            return app.utils.gen_response(400, traceback.format_exc())
    return app.utils.gen_response(405)


def video_label(request):
    if request.method == 'GET':
        try:
            open_id = request.GET.get('open_id')
            user = User.objects.get(open_id=open_id)
            add = request.GET.get('add')
            video_list = user.video.all()
            res = []
            for i in video_list:
                if add == 0:
                    i.labels = ''
                    i.save()
                res.append({'video': i.photo_id, 'label': i.labels})
            labels = Label.objects.all()
            for label in labels:
                res.append({
                    'name': label.user.name,
                    'label': label.label_name,
                    'num': label.num
                })
                if add == 0:
                    label.delete()
            return app.utils.gen_response(200, res)
        except Exception:
            return app.utils.gen_response(400, traceback.format_exc())
    return app.utils.gen_response(405)
