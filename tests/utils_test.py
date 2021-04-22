'''
this file should be a .py file as tests for login function
'''
import unittest
from datetime import datetime
import app.utils
import app.times
from app.models import User, Video, AnalyseHour, Analyse
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
            user = test_user,
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

    def tearDown(self):
        User.objects.filter(open_id="utils").delete()
