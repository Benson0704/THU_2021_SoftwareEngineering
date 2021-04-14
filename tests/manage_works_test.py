'''
this file should be a .py file as tests for manageWorks module
finished: 4.7
'''
from django.test import TestCase
from app.models import User, Video, Label
import pytest
import app.times
import app.utils
from datetime import datetime


@pytest.mark.django_db
class TestManageWorks(TestCase):
    '''
    This is a unittest for manageWorks
    '''
    def setUp(self):
        """
        this is the constructin of tests
        """
        User.objects.filter(open_id="todayissunny").delete()
        brisa = User.objects.create(open_id="todayissunny",
                                    name="brisa",
                                    sex=0,
                                    head="https://ThisGirlIsBeautiful",
                                    bigHead="",
                                    city="Chengdu",
                                    fan=40,
                                    follow=40,
                                    video_count=2,
                                    public_count=2,
                                    friend_count=0,
                                    private_count=0,
                                    total_like_count=60,
                                    total_comment_count=30,
                                    total_view_count=120,
                                    access_token="9XZzf6up5SH8U1JFUKs=\n",
                                    refresh_token="9XZzf6up5SH8U1JFUKs=\n")
        brisa.save()
        Video.objects.filter(
            photo_id='this is a sunrise photo in Hogwards').delete()
        new_video = Video.objects.create(
            user=brisa,
            photo_id="this is a sunrise photo in Hogwards",
            caption="hogwards sunrise",
            cover="https://HogwardsSunrise",
            play_url="https://PlayHogwardsSunrise",
            create_time='2022-04-07 12:13:15',
            like_count=30,
            comment_count=15,
            view_count=60,
            pending=False,
            labels="")
        new_video.save()
        Video.objects.filter(photo_id='this is a photo on Earth').delete()
        new_video = Video.objects.create(user=brisa,
                                         photo_id="this is a photo on Earth",
                                         caption="Earth view",
                                         cover="https://EarthView",
                                         play_url="https://PlayEarthView",
                                         create_time='2022-04-07 12:13:17',
                                         like_count=30,
                                         comment_count=15,
                                         view_count=60,
                                         pending=False,
                                         labels="")
        new_video.save()
        Label.objects.filter(label_name='scene').delete()
        new_label = Label.objects.create(user=brisa, label_name="scene", num=0)
        new_label.save()

    def test_get_video_time_openid_lost(self):
        """
        this is a test for get_video_time(error:openid lost)
        """
        payload = {
            'begin_timestamp': 00000000000,
            'end_timestamp': 00000000000,
            'count_per_page': 5,
            'page': 3,
        }
        response = self.client.get('/api/video/time',
                                   data=payload,
                                   content_type="application/json")
        self.assertEqual(400, response.json()['code'])

    def test_get_video_time(self):
        """
        this is a test for get_video_time(no error)
        """
        time1 = datetime(2022, 4, 7, 12, 13, 10)
        time2 = datetime(2022, 4, 7, 12, 13, 20)
        payload = {
            'open_id': "todayissunny",
            'begin_timestamp': app.times.datetime2timestamp(time1),
            'term_timestamp': app.times.datetime2timestamp(time2),
            'count_per_page': 5,
            'page': 1,
        }
        time3 = datetime(2022, 4, 7, 12, 13, 17)
        time4 = datetime(2022, 4, 7, 12, 13, 15)
        expected_vedioslists = [
            {
                "photo_id": "this is a photo on Earth",
                "caption": "Earth view",
                "cover": "https://EarthView",
                "play_url": "https://PlayEarthView",
                "create_time": app.times.datetime2timestamp(time3),
                "like_count": 30,
                "comment_count": 15,
                "view_count": 60,
                "pending": False,
                "labels": [""]
            }, {
                "photo_id": "this is a sunrise photo in Hogwards",
                "caption": "hogwards sunrise",
                "cover": "https://HogwardsSunrise",
                "play_url": "https://PlayHogwardsSunrise",
                "create_time": app.times.datetime2timestamp(time4),
                "like_count": 30,
                "comment_count": 15,
                "view_count": 60,
                "pending": False,
                "labels": [""]
            }]
        response = self.client.get('/api/video/time',
                                   data=payload,
                                   content_type="application/json")
        self.assertEqual(200, response.json()['code'])
        self.assertEqual(response.json()['data']['video_list'],
                         expected_vedioslists)

    def test_get_label_list_get_openid_lost(self):
        """
        this is a test for get_label_list(method: get, error: openid lost)
        """
        response = self.client.get('/api/video/label',
                                   content_type="application/json")
        self.assertEqual(400, response.json()['code'])

    def test_get_label_list_post_openid_lost(self):
        """
        this is a test for get_label_list(method: post, error: openid lost)
        """
        response = self.client.post('/api/video/label',
                                    content_type="application/json")
        self.assertEqual(400, response.json()['code'])

    def test_get_label_list_get(self):
        """
        this is a test for get_label_list(method: get, no error)
        """
        payload = {"open_id": "todayissunny"}
        response = self.client.get('/api/video/label',
                                   data=payload,
                                   content_type="application/json")
        expected_labels = [{"label": "scene", "num": 0}]
        self.assertEqual(200, response.json()['code'])
        self.assertEqual(response.json()['data']['label_list'],
                         expected_labels)

    def test_get_label_list_post(self):
        """
        this is a test for get_label_list(add labels, method: post, no error)
        """
        payload = {
            "open_id": "todayissunny",
            "photo_id": "this is a Sunrise photo in Hogwards",
            "label": "scene",
            "add": 1
        }
        self.client.post('/api/video/label',
                         data=payload,
                         content_type="application/json")
        payload = {
            "open_id": "todayissunny",
            "photo_id": "this is a photo on Earth",
            "label": "scene",
            "add": 1
        }
        response = self.client.post('/api/video/label',
                                    data=payload,
                                    content_type="application/json")
        self.assertEqual(201, response.json()['code'])
        label = Label.objects.get(
            user=User.objects.get(open_id='todayissunny'),
            label_name="scene")
        self.assertEqual(label.num, 2)
        payload = {
            "open_id": "todayissunny",
            "photo_id": "this is a Sunrise photo in Hogwards",
            "label": "magic",
            "add": 1
        }
        response = self.client.post('/api/video/label',
                                    data=payload,
                                    content_type="application/json")
        self.assertEqual(201, response.json()['code'])
        label = Label.objects.get(
            user=User.objects.get(open_id='todayissunny'),
            label_name="magic")
        self.assertEqual(label.num, 1)
        payload = {
            "open_id": "todayissunny",
            "photo_id": "this is a Sunrise photo in Hogwards",
            "label": "scene",
            "add": 0
        }
        self.client.post('/api/video/label',
                         data=payload,
                         content_type="application/json")
        payload = {
            "open_id": "todayissunny",
            "photo_id": "this is a photo on Earth",
            "label": "scene",
            "add": 0
        }
        response = self.client.post('/api/video/label',
                                    data=payload,
                                    content_type="application/json")
        self.assertEqual(201, response.json()['code'])
        label = Label.objects.filter(
            user=User.objects.get(open_id='todayissunny'),
            label_name="scene")
        self.assertFalse(label)

    def tearDown(self):
        """
        this is for destruction of tests
        """
        User.objects.filter(open_id="todayissunny").delete()
