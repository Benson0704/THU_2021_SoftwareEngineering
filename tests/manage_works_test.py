'''
this file should be a .py file as tests for manageWorks function
'''
from django.test import TestCase, Client
import manageWorks.views
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
        User.objects.filter(open_id="todayisagoodday").delete()
        brisa = User.objects.create(open_id="todayisagoodday",
                                    name="brisa",
                                    sex=1,
                                    head="https://ThisIsABeautifulGirl",
                                    bigHead="",
                                    city="Shanghai",
                                    fan=20,
                                    follow=20,
                                    video_count=2,
                                    public_count=2,
                                    friend_count=0,
                                    private_count=0,
                                    total_like_count=20,
                                    total_comment_count=10,
                                    total_view_count=40,
                                    access_token="9XZzf6up5SH8U1JFUKs=\n",
                                    refresh_token="9XZzf6up5SH8U1JFUKs=\n")
        brisa.save()
        Video.objects.filter(
            photo_id='this is a sunset photo in Hogwards').delete()
        new_video = Video.objects.create(
            user=brisa,
            photo_id="this is a sunset photo in Hogwards",
            caption="hogwards sunset",
            cover="https://HogwardsSunset",
            play_url="https://PlayHogwardsSunset",
            create_time='2022-04-07 12:13:14',
            like_count=10,
            comment_count=5,
            view_count=20,
            pending=False,
            labels="")
        new_video.save()
        Video.objects.filter(photo_id='this is a photo on Mars').delete()
        new_video = Video.objects.create(user=brisa,
                                         photo_id="this is a photo on Mars",
                                         caption="Mars view",
                                         cover="https://MarsView",
                                         play_url="https://PlayMarsView",
                                         create_time='2022-04-07 12:13:16',
                                         like_count=10,
                                         comment_count=5,
                                         view_count=20,
                                         pending=False,
                                         labels="")
        new_video.save()
        new_label = Label.objects.create(user=brisa, label_name="scene", num=0)
        new_label.save()

    def test_get_video_time_openid_lost(self):
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
        time1 = datetime(2022, 4, 7, 12, 13, 10)
        time2 = datetime(2022, 4, 7, 12, 13, 20)
        payload = {
            'open_id': "todayisagoodday",
            'begin_timestamp': app.times.datetime2timestamp(time1),
            'end_timestamp': app.times.datetime2timestamp(time2),
            'count_per_page': 5,
            'page': 1,
        }
        expected_vedioslists = [{
            "photo_id": "this is a sunset photo in Hogwards",
            "caption": "hogwards sunset",
            "cover": "https://HogwardsSunset",
            "play_url": "https://PlayHogwardsSunset",
            "create_time": '2022-04-07 12:13:14',
            "like_count": 10,
            "comment_count": 5,
            "view_count": 20,
            "pending": False,
            "labels": ""
        }, {
            "photo_id": "this is a photo on Mars",
            "caption": "Mars view",
            "cover": "https://MarsView",
            "play_url": "https://PlayMarsView",
            "create_time": '2022-04-07 12:13:16',
            "like_count": 10,
            "comment_count": 5,
            "view_count": 20,
            "pending": False,
            "labels": ""
        }]
        response = self.client.get('/api/video/time',
                                   data=payload,
                                   content_type="application/json")
        self.assertEqual(200, response.json()['code'])
        self.assertEqual(response['data'], expected_vedioslists)

    def test_get_label_list_get_openid_lost(self):
        payload = {}
        response = self.client.get('/api/video/label',
                                   data=payload,
                                   content_type="application/json")
        self.assertEqual(400, response.json()['code'])

    def test_get_label_list_post_openid_lost(self):
        payload = {}
        response = self.client.post('/api/video/label',
                                    data=payload,
                                    content_type="application/json")
        self.assertEqual(400, response.json()['code'])

    def test_get_label_list_get(self):
        payload = {"open_id": "todayisagoodday"}
        response = self.client.get('/api/video/label/',
                                   data=payload,
                                   content_type="application/json")
        expected_labels = [{"label": "scene", "num": 0}]
        self.assertEqual(200, response.json())
        self.assertEqual(response.json()['data'], expected_labels)

    def test_get_label_list_post(self):
        payload = {
            "open_id": "todayisagoodday",
            "photo_id": "this is a sunset photo in Hogwards",
            "label": "scene",
            "add": 1
        }
        response = self.client.post('/api/video/label',
                                    data=payload,
                                    content_type="application/json")
        self.assertEqual(201, response.json()['code'])
        label = Label.objects.get(label_name="scene")
        self.assertEqual(label.num, 1)

    def tearDown(self):
        Label.objects.filter(label_name="scene").delete()
        User.objects.filter(open_id="todayisagoodday").delete()
