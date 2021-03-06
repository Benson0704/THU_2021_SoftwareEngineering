'''
this file should be a .py file as tests for notice module
finished: 4.22
'''
from datetime import datetime
from django.test import TestCase
import pytest
from app.models import User, Warn, Notice
import app.times


@pytest.mark.django_db
class TestNotice(TestCase):
    '''
    This is a unittest for notice module
    '''
    def setUp(self):
        """
        this is the construction for notice test
        """
        test_user = User.objects.create(open_id="test user", name="test user")
        test_user.save()
        test_user = User.objects.create(open_id="another test user",
                                        name="another test user")
        test_user.save()
        test_notice = Notice.objects.create(publish_user="test user",
                                            title="test title",
                                            create_time='2022-04-07 12:13:14',
                                            content="test content")
        test_notice.save()
        test_notice = Notice.objects.create(publish_user="another test user",
                                            title="test title",
                                            create_time='2022-04-09 12:13:14',
                                            content="test content")
        test_notice.save()
        test_warn = Warn.objects.create(user=test_user,
                                        warn_time='2022-04-09 12:13:15')
        test_warn.save()

    def test_get_notice_user(self):
        """
        this is a test for get_notice_user
        method: get  error: none
        """
        payload = {}
        response = self.client.get('/api/notice/user',
                                   data=payload,
                                   content_type="application/json")
        notices = response.json()['data']['notices']
        notice_titles = []
        for notice in notices:
            notice_titles.append(notice['title'])
        expected_title = "test title"
        self.assertEqual(200, response.json()['code'])
        self.assertTrue(expected_title in notice_titles)

    def test_get_flows_post(self):
        """
        this is a test for get_flows
        method: post
        """
        payload = {
            'open_id': "test user",
            'limit': 10
        }
        response = self.client.post('/api/notice/flows',
                                    data=payload,
                                    content_type="application/json")
        self.assertEqual(response.json()['code'], 200)
        user = User.objects.get(open_id="test user")
        self.assertEqual(10, user.limit)

    def test_get_flows_get(self):
        """
        this is a test for get_flows
        method: post
        """
        payload = {
            'open_id': "test user",
        }
        response = self.client.get('/api/notice/flows',
                                   data=payload,
                                   content_type="application/json")
        self.assertEqual(response.json()['code'], 200)
        user = User.objects.get(open_id="test user")
        self.assertEqual(20, user.limit)

    def test_get_flows_post_limit_lost(self):
        """
        this is a test for get_flows
        method: post  error: limit lost
        """
        payload = {}
        response = self.client.post('/api/notice/flows',
                                    data=payload,
                                    content_type="application/json")
        self.assertEqual(response.json()['code'], 400)

    def test_get_flows_get_openid_lost(self):
        """
        this is a test for get_flows
        method: get  error: openid lost
        """
        payload = {}
        response = self.client.get('/api/notice/flows',
                                   data=payload,
                                   content_type="application/json")
        self.assertEqual(response.json()['code'], 400)

    def test_operate_notice_admin_get(self):
        """
        this is a test for operate_notice_admin
        method: get
        """
        payload = {"open_id": "test user"}
        response = self.client.get('/api/notice/admin',
                                   data=payload,
                                   content_type="application/json")
        my_notices = response.json()['data']['my_notices']
        other_notices = response.json()['data']['other_notices']
        notice_titles = []
        for notice in other_notices:
            notice_titles.append(notice['title'])
        expected_title = "test title"
        self.assertEqual(200, response.json()['code'])
        self.assertEqual(expected_title, my_notices[0]['title'])
        self.assertTrue(expected_title in notice_titles)

    def test_operate_notice_admin_get_id_lost(self):
        """
        this is a test for operate_notice_admin
        method: get error: id_lost
        """
        payload = {}
        response = self.client.get('/api/notice/admin',
                                   data=payload,
                                   content_type="application/json")
        self.assertEqual(400, response.json()['code'])

    def test_operate_notice_admin_post_id_lost(self):
        """
        this is a test for operate_notice_admin
        method: post  error: id lost
        """
        payload = {}
        response = self.client.post('/api/notice/admin',
                                    data=payload,
                                    content_type="application/json")
        self.assertEqual(400, response.json()['code'])

    def test_operate_notice_admin_post_add(self):
        """
        this is a test for operate_notice_admin
        method: post  error: none
        """
        time = datetime(2022, 3, 4, 12, 13, 11)
        payload = {
            'open_id': "test user",
            'timestamp': app.times.datetime2timestamp(time),
            'content': "new notice",
            'title': "new title",
            'add': 1
        }
        response = self.client.post('/api/notice/admin',
                                    data=payload,
                                    content_type="application/json")
        self.assertEqual(200, response.json()['code'])
        notice = Notice.objects.get(content="new notice")
        self.assertTrue(notice)

    def test_operate_notice_admin_post_delete(self):
        """
        this is a test for operate_notice_admin
        method: post  error: none
        """
        time = datetime(2022, 4, 7, 12, 13, 14)
        payload = {
            'open_id': "test user",
            'timestamp': app.times.datetime2timestamp(time),
            'content': "test content",
            'title': "test title",
            'add': 0
        }
        response = self.client.post('/api/notice/admin',
                                    data=payload,
                                    content_type="application/json")
        self.assertEqual(200, response.json()['code'])

    def tearDown(self):
        """
        this is the deconstruction for notice tests
        """
        User.objects.filter(open_id="test user").delete()
        Notice.objects.filter(publish_user="test user").delete()
