'''
this file should be a .py file as tests for analyseWorks module
finished: 4.15
'''
from django.test import TestCase
from app.models import User, Video, Analyse
import pytest
import app.times
from datetime import datetime


@pytest.mark.django_db
class TestAnalyseWorks(TestCase):
    '''
    This is a unittest for analyseWorks
    '''
    def setUp(self):
        """
        this is the constructin of tests
        """
        User.objects.filter(open_id="justhavesomefun").delete()
        brisa = User.objects.create(open_id="justhavesomefun",
                                    name="brisa",
                                    sex=1,
                                    video_count=1,
                                    public_count=1)
        brisa.save()
        Video.objects.filter(
            photo_id='this is a sunrise photo in Hogwards').delete()
        new_video = Video.objects.create(
            user=brisa,
            photo_id="Welcome to world 1st university",
            caption="World 1st university",
            cover="https://World1stuniversity",
            play_url="https://PlayWorld1stuniversity",
            create_time='2022-04-07 12:13:15',
            like_count=20,
            comment_count=10,
            view_count=40,
            pending=False,
            labels="")
        new_video.save()
        new_analyse = Analyse.objects.create(
            video=new_video,
            user_id="justhavesomefun",
            sum_time='2022-04-08 00:00:00',
            total_view_count=5,
            total_like_count=2,
            total_comment_count=1)
        new_analyse.save()
        new_analyse = Analyse.objects.create(
            video=new_video,
            user_id="justhavesomefun",
            sum_time='2022-04-09 00:00:00',
            total_view_count=12,
            total_like_count=5,
            total_comment_count=3)
        new_analyse.save()
        new_analyse = Analyse.objects.create(
            video=new_video,
            user_id="justhavesomefun",
            sum_time='2022-04-10 00:00:00',
            total_view_count=16,
            total_like_count=7,
            total_comment_count=5)
        new_analyse.save()
        new_analyse = Analyse.objects.create(
            video=new_video,
            user_id="justhavesomefun",
            sum_time='2022-04-11 00:00:00',
            total_view_count=22,
            total_like_count=10,
            total_comment_count=7)
        new_analyse.save()
        new_analyse = Analyse.objects.create(
            video=new_video,
            user_id="justhavesomefun",
            sum_time='2022-04-12 00:00:00',
            total_view_count=27,
            total_like_count=12,
            total_comment_count=8)
        new_analyse.save()
        new_analyse = Analyse.objects.create(
            video=new_video,
            user_id="justhavesomefun",
            sum_time='2022-04-13 00:00:00',
            total_view_count=32,
            total_like_count=15,
            total_comment_count=9)
        new_analyse.save()
        new_analyse = Analyse.objects.create(
            video=new_video,
            user_id="justhavesomefun",
            sum_time='2022-04-14 00:00:00',
            total_view_count=40,
            total_like_count=20,
            total_comment_count=10)
        new_analyse.save()

    def test_get_videos_info_by_time_photoid_lost(self):
        """
        this is a test for get_videos_info_by_time(error:openid_lost)
        """
        payload = {
            'begin_timestamp': 00000000000,
            'term_timestamp': 00000000000,
        }
        response = self.client.get('/api/analysis/single',
                                   data=payload,
                                   content_type="application/json")
        self.assertEqual(400, response.json()['code'])

    def test_get_videos_info_by_time(self):
        """
        this is a test for get_videos_info_by_time
        """
        time1 = datetime(2022, 4, 12, 0, 0, 0)
        time2 = datetime(2022, 4, 12, 23, 59, 59)
        payload = {
            'photo_id': "Welcome to world 1st university",
            'begin_timestamp': app.times.datetime2timestamp(time1),
            'term_timestamp': app.times.datetime2timestamp(time2),
        }
        expected_res = {}
        expected_res['photo_id'] = "Welcome to world 1st university"
        expected_res['caption'] = "World 1st university"
        expected_res['cover'] = "https://World1stuniversity"
        expected_res['play_url'] = "https://PlayWorld1stuniversity"
        expected_res['create_time'] = '2022-04-07T12:13:15'
        expected_res['pending'] = False
        expected_res['like_count'] = 20
        expected_res['comment_count'] = 10
        expected_res['view_count'] = 40
        expected_count_list = []
        temp = {
            'like_count': 3,
            'comment_count': 1,
            'view_count': 5
        }
        expected_count_list.append(temp)
        expected_res['count_list'] = expected_count_list
        response = self.client.get('/api/analysis/single',
                                   data=payload,
                                   content_type="application/json")
        self.assertEqual(200, response.json()['code'])
        self.assertEqual(expected_res, response.json()['data'])

    def test_get_all_videos_info_openid_lost(self):
        """
        this is a test for get_all_videos_info(error:openid_lost)
        """
        payload = {
            'begin_timestamp': 00000000000,
            'term_timestamp': 00000000000,
        }
        response = self.client.get('/api/analysis/global_day',
                                   data=payload,
                                   content_type="application/json")
        self.assertEqual(400, response.json()['code'])

    def test_get_all_videos_info(self):
        """
        this is a test for get_all_videos_info
        """
        time1 = datetime(2022, 4, 13, 0, 0, 0)
        time2 = datetime(2022, 4, 13, 23, 59, 59)
        payload = {
            'open_id': "justhavesomefun",
            'begin_timestamp': app.times.datetime2timestamp(time1),
            'term_timestamp': app.times.datetime2timestamp(time2),
        }
        expected_recent_data = {
            'like_count': 10,
            'comment_count': 3,
            'view_count': 18
        }
        expected_count_list = [{
            'like_count': 5,
            'comment_count': 1,
            'view_count': 8
        }]
        response = self.client.get('/api/analysis/global_day',
                                   data=payload,
                                   content_type="application/json")
        self.assertEqual(200, response.json()['code'])
        self.assertEqual(expected_recent_data,
                         response.json()['data']['recent_data'])
        self.assertEqual(expected_count_list,
                         response.json()['data']['count_list'])

    def tearDown(self):
        """
        this is for destruction of tests
        """
        User.objects.filter(open_id="justhavesomefun").delete()
