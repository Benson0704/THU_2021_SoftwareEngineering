'''
this file should be a .py file as tests for login function
finished: 4.22
'''
import unittest
from datetime import datetime
import app.utils
import app.times
from app.models import User, Video, AnalyseHour, Analyse, Warn
import pytest


@pytest.mark.django_db
class TestUtils(unittest.TestCase):
    """
    This is a unittest for analyseWorks
    """
    def setUp(self):
        """
        this is the constructin of tests for utils
        """
        test_user = User.objects.create(open_id="utils",
                                        name="test utils")
        test_user.save()
        test_video = Video.objects.create(
            user=test_user,
            photo_id="test utils videos",
            play_url="test utils play_url",
            pending=False,
            create_time="2021-06-07 13:12:11")
        test_video.save()

    def test_analyse_hour_data(self):
        """
        this is a test for analyse_hour_data
        """
        open_id = "utils"
        time = datetime(2021, 6, 7, 14, 0, 0)
        video_list = [{
            'photo_id': "test utils videos",
            'view_count': 10,
            'like_count': 5,
            'comment_count': 3
        }]
        app.utils.analyse_hour_data(open_id, video_list, time)
        analysis = AnalyseHour.objects.get(user_id="utils")
        print(AnalyseHour.objects.all())
        self.assertTrue(analysis)

    def test_analyse_daily_data(self):
        """
        this is a test for analyse_daily_data
        """
        open_id = "utils"
        time = "2021-06-07 14:00:00"
        video_list = [{
            'photo_id': "test utils videos",
            'view_count': 10,
            'like_count': 5,
            'comment_count': 3
        }]
        app.utils.analyse_daily_data(open_id, video_list, time)
        analysis = Analyse.objects.get(user_id="utils")
        self.assertTrue(analysis)

    def test_store_flow(self):
        """
        this is a test for store_flow
        """
        tvideo = Video.objects.get(photo_id="test utils videos")
        tuser = User.objects.get(open_id="utils")
        open_id = "utils"
        time1 = datetime(2021, 3, 7, 0, 0, 0)
        time2 = datetime(2021, 3, 6, 0, 0, 0)
        time3 = datetime(2021, 3, 6, 23, 0, 0)
        one_day_before_time = app.times.datetime2timestamp(time2)
        one_hour_before_time = app.times.datetime2timestamp(time3)
        now_time = app.times.datetime2timestamp(time1)
        analyse1 = AnalyseHour.objects.create(video=tvideo,
                                              user_id="utils",
                                              sum_time="2021-03-07 00:00:00",
                                              total_comment_count=20,
                                              total_like_count=40,
                                              total_view_count=100)
        analyse1.save()
        analyse2 = AnalyseHour.objects.create(video=tvideo,
                                              user_id="utils",
                                              sum_time="2021-03-06 00:00:00",
                                              total_comment_count=10,
                                              total_like_count=20,
                                              total_view_count=40)
        analyse2.save()
        analyse3 = AnalyseHour.objects.create(video=tvideo,
                                              user_id="utils",
                                              sum_time="2021-03-06 23:00:00",
                                              total_comment_count=18,
                                              total_like_count=24,
                                              total_view_count=88)
        analyse3.save()
        app.utils.store_flow(open_id,
                             one_day_before_time,
                             one_hour_before_time,
                             now_time)
        warn = Warn.objects.get(user=tuser)
        self.assertTrue(warn)
        Warn.objects.filter(user=tuser).delete()

    def tearDown(self):
        """
        this is the deconstruction for tests
        """
        User.objects.filter(open_id="utils").delete()
