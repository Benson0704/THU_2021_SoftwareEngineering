'''
this file should be a .py file as tests for feedback module
'''
from django.test import TestCase
from app.models import User, Message, Feedback
import app.times
import pytest
from datetime import datetime


@pytest.mark.django_db
class TestAppTimes(TestCase):
    '''
    This is a unittest for feedback module
    '''
    def setUp(self):
        """
        this is the constructin of tests for feedback
        """
        User.objects.filter(open_id="feedbackuser").delete()
        User.objects.filter(open_id="feedbackmanager").delete()
        feedback_user = User.objects.create(open_id="feedbackuser",
                                            name="feedback_user")
        feedback_manager = User.objects.create(open_id="feedbackmanager",
                                               name="feedback_manager",
                                               identity=True)
        feedback_user.save()
        feedback_manager.save()
        message_solved = Message.objects.create(content="message solved",
                                                title="title",
                                                create_time="2021-06-05 11:11:11",
                                                user=feedback_user,
                                                status=True,
                                                manager="feedbackmanager")
        message_unsolved = Message.objects.create(content="message unsolved",
                                                  title="untitle",
                                                  create_time="2021-06-06 11:11:11",
                                                  user=feedback_user,
                                                  status=False)
        message_solved.save()
        message_unsolved.save()
        feedback = Feedback.objects.create(message=message_solved,
                                           content="feedback content",
                                           title="feedback title",
                                           create_time="2021-06-05 21:11:11",
                                           manager="feedbackmanager",
                                           user="user")
        feedback.save()

    # def test_operate_feedback_user_get_openid_lost(self):
    #     """
    #     this is a test for operate_feedback_user
    #     method: get  error: openid lost
    #     """
    #     payload = {}
    #     response = self.client.get('/api/feedback/user',
    #                                data=payload,
    #                                content_type="application/json")
    #     self.assertEqual(400, response.json()['code'])

    # def test_operate_feedback_user_get(self):
    #     """
    #     this is a test for operate_feedback_user
    #     method: get  error: none
    #     """
    #     payload = {
    #         'open_id': "feedbackuser"
    #     }
    #     time1 = datetime(2021, 6, 6, 11, 11, 11)
    #     time2 = datetime(2021, 6, 5, 11, 11, 11)
    #     time3 = datetime(2021, 6, 5, 21, 11, 11)
    #     response = self.client.get('/api/feedback/user',
    #                                data=payload,
    #                                content_type="application/json")
    #     expected_unsolved_list = [{
    #         'title': 'untitle',
    #         'content': "message unsolved",
    #         'timestamp': app.times.datetime2timestamp(time1)
    #     }]
    #     expected_solved_list = [{
    #         'title': 'title',
    #         'content': "message solved",
    #         'timestamp': app.times.datetime2timestamp(time2),
    #         'admin_name': "feedbackmanager",
    #         'response': "feedback content",
    #         'response_timestamp': app.times.datetime2timestamp(time3)
    #     }]
    #     self.assertEqual(200, response.json()['code'])
    #     self.assertEqual(expected_unsolved_list,
    #                      response.json()['data']['data']['unsolved_feedbacks'])
    #     self.assertEqual(expected_solved_list,
    #                      response.json()['data']['data']['solved_feedbacks'])

    # def test_operate_feedback_user_post_openid_lost(self):
    #     """
    #     this is a test for operate_feedback_user
    #     method: post  error: openid lost
    #     """
    #     payload = {}
    #     response = self.client.post('/api/feedback/user',
    #                                 data=payload,
    #                                 content_type="application/json")
    #     self.assertEqual(400, response.json()['code'])

    # def test_operate_feedback_user_post(self):
    #     """
    #     this is a test for operate_feedback_user
    #     method: post
    #     """
    #     time = datetime(2021, 6, 12, 21, 11, 11)
    #     payload = {
    #         'open_id': "feedbackuser",
    #         'timestamp': app.times.datetime2timestamp(time),
    #         'content': "test content",
    #         'title': "test title"
    #     }
    #     response = self.client.post('/api/feedback/user',
    #                                 data=payload,
    #                                 content_type="application/json")
    #     self.assertEqual(200, response.json()['code'])
    #     message = Message.objects.get(title="test title")
    #     self.assertEqual(message.content, "test content")

    def teardown(self):
        """
        this is the deconstructin of tests for feedback
        """
        User.objects.filter(open_id="feedbackuser").delete()
        User.objects.filter(open_id="feedbackmanager").delete()
        Message.objects.filter(title="test title").delete()
