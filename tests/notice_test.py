'''
this file should be a .py file as tests for notice module
'''
from django.test import TestCase
from app.models import User, Message, Feedback
import app.times
import pytest
from datetime import datetime


@pytest.mark.django_db
class TestNotice(TestCase):
    '''
    This is a unittest for notice module
    '''
    def setUp(self):

    def test_get_notice_user(self):
        """
        this is a test for get_notice_user
        method: get  error: openid lost
        """
        payload = {}
        response = self.client.get('/api/notice/user',
                                   data=payload,
                                   content_type="application/json")
        self.assertEqual(400, response.json()['code'])
