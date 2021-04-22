'''
this file should be a .py file as tests for notice module
finished: 4.22
'''
from django.test import TestCase
from app.models import User, Warn, Notice
import app.times
import pytest
from datetime import datetime


@pytest.mark.django_db
class TestNotice(TestCase):
    '''
    This is a unittest for notice module
    '''
    def setUp(self):
        """
        this is the construction for notice test
        """
        test_user = User.objects.create(open_id="test user",
                                        name="test user")
        test_user.save()
        test_notice = Notice.objects.create(publish_user="test user",
                                            title="test title",
                                            create_time='2022-04-07 12:13:14',
                                            content="test content")
        test_notice.save()
        test_warn = Warn.objects.create(user=test_user,
                                        warn_time='2022-04-09 12:13:15')
        test_warn.save()

    def test_get_notice_user_openid_lost(self):
        """
        this is a test for get_notice_user
        method: get  error: openid lost
        """
        payload = {}
        response = self.client.get('/api/notice/user',
                                   data=payload,
                                   content_type="application/json")
        self.assertEqual(400, response.json()['code'])

    def test_get_notice_user(self):
        """
        this is a test for get_notice_user
        method: get  error: none
        """
        payload = {
            'open_id': "test user"
        }
        response = self.client.get('/api/notice/user',
                                   data=payload,
                                   content_type="application/json")
        print(response.json()['code'])
        notices = response.json()['data']['notices']
        notice_titles = []
        for notice in notices:
            notice_titles.append(notice['title'])
        expected_title = "test title"
        self.assertEqual(200, response.json()['code'])
        self.assertTrue(expected_title in notice_titles)

    def test_operate_notice_admin_get(self):
        """
        this is a test for operate_notice_admin
        method: get
        """
        response = self.client.get('/api/notice/admin',
                                   content_type="application/json")
        notices = response.json()['data']['notices']
        notice_titles = []
        for notice in notices:
            notice_titles.append(notice['title'])
        expected_title = "test title"
        self.assertEqual(200, response.json()['code'])
        self.assertTrue(expected_title in notice_titles)

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

    def test_operate_notice_admin_post(self):
        """
        this is a test for operate_notice_admin
        method: post  error: none
        """
        time = datetime(2022, 3, 4, 12, 13, 11)
        payload = {
            'open_id': "test user",
            'timestamp': app.times.datetime2timestamp(time),
            'content': "new notice",
            'title': "new title"
        }
        response = self.client.post('/api/notice/admin',
                                    data=payload,
                                    content_type="application/json")
        self.assertEqual(200, response.json()['code'])
        notice = Notice.objects.get(content="new notice")
        self.assertTrue(notice)

    def tearDown(self):
        """
        this is the deconstruction for notice tests
        """
        User.objects.filter(open_id="test user").delete()
        Notice.objects.filter(publish_user="test user").delete()
