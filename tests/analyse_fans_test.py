'''
this file should be a .py file as tests for analyseFans module
finished: 4.22
'''


from django.test import TestCase
from app.models import User, Video, AnalyseHour
import app.times
import pytest
from datetime import datetime


@pytest.mark.django_db
class TestAnalyseFans(TestCase):
    '''
    This is a unittest for analyseFans
    '''
    def setUp(self):
        '''
        this is constructin of tests for analyse fans
        '''
        User.objects.filter(open_id="Icannotmakeupanewname").delete()
        brisa3 = User.objects.create(open_id="Icannotmakeupanewname",
                                     name="brisa3",
                                     sex=1,
                                     video_count=1,
                                     public_count=1)
        brisa3.save()
        Video.objects.filter(
            photo_id='today is dropping dirt').delete()
        new_video = Video.objects.create(
            user=brisa3,
            photo_id="today is dropping dirt",
            caption="Dirt Dropping",
            cover="https://DirtDropping",
            play_url="https://PlayDirtDropping",
            create_time='2022-04-05 08:04:19',
            like_count=5,
            comment_count=3,
            view_count=12,
            pending=False,
            labels="")
        new_video.save()

    def test_get_fans_info_openid_lost(self):
        """
        this is a test for get_fans_info(error:openid_lost)
        """
        payload = {
            'begin_timestamp': 00000000000,
            'term_timestamp': 00000000000,
        }
        response = self.client.get('/api/analysis/globalhour',
                                   data=payload,
                                   content_type="application/json")
        self.assertEqual(400, response.json()['code'])

    def test_get_fans_info_double(self):
        """
        this is a test for get_fans_info
        """
        new_video = Video.objects.get(photo_id="today is dropping dirt")
        new_analysisHour = AnalyseHour.objects.create(
            video=new_video,
            user_id="Icannotmakeupanewname",
            sum_time="2022-04-05 09:00:00",
            total_comment_count=1,
            total_like_count=2,
            total_view_count=5
        )
        new_analysisHour.save()
        new_analysisHour = AnalyseHour.objects.create(
            video=new_video,
            user_id="Icannotmakeupanewname",
            sum_time="2022-04-05 10:00:00",
            total_comment_count=2,
            total_like_count=4,
            total_view_count=7
        )
        new_analysisHour.save()
        time1 = datetime(2022, 4, 5, 9, 0, 0)
        time2 = datetime(2022, 4, 5, 10, 0, 0)
        payload = {
            'open_id': "Icannotmakeupanewname",
            'begin_timestamp': app.times.datetime2timestamp(time1),
            'term_timestamp': app.times.datetime2timestamp(time2),
        }
        response = self.client.get('/api/analysis/globalhour',
                                   data=payload,
                                   content_type="application/json")
        expected_count_list = [{
            'view_count': 2,
            'comment_count': 1,
            'like_count': 2
        }]
        self.assertEqual(200, response.json()['code'])
        self.assertEqual(expected_count_list,
                         response.json()['data']['count_list'])
        AnalyseHour.objects.filter(video=new_video).delete()

    def test_get_fans_info_single(self):
        """
        this is a test for get_fans_info
        """
        new_video = Video.objects.get(photo_id="today is dropping dirt")
        new_analysisHour = AnalyseHour.objects.create(
            video=new_video,
            user_id="Icannotmakeupanewname",
            sum_time="2022-04-05 12:00:00",
            total_comment_count=3,
            total_like_count=5,
            total_view_count=12
        )
        new_analysisHour.save()
        time1 = datetime(2022, 4, 5, 11, 0, 0)
        time2 = datetime(2022, 4, 5, 12, 0, 0)
        payload = {
            'open_id': "Icannotmakeupanewname",
            'begin_timestamp': app.times.datetime2timestamp(time1),
            'term_timestamp': app.times.datetime2timestamp(time2),
        }
        response = self.client.get('/api/analysis/globalhour',
                                   data=payload,
                                   content_type="application/json")
        expected_count_list = [{
            'view_count': 12,
            'comment_count': 3,
            'like_count': 5
        }]
        self.assertEqual(200, response.json()['code'])
        self.assertEqual(expected_count_list,
                         response.json()['data']['count_list'])
        AnalyseHour.objects.filter(video=new_video).delete()

    def tearDown(self):
        """
        this is for destruction of tests
        """
        User.objects.filter(open_id="Icannotmakeupanewname").delete()
