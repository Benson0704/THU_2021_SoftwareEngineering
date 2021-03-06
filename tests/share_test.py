'''
this file should be a .py file as tests for share module
finish: 4.22, add timestamp
'''
from datetime import datetime
import pytest
from django.test import TestCase
from app.models import User
import app.times


@pytest.mark.django_db
class TestShare(TestCase):
    '''
    This is a unittest for share module
    '''
    def setUp(self):
        '''
        This is the construction of unittests for share module
        '''
        User.objects.filter(open_id="test sharer").delete()
        User.objects.filter(open_id="test shared").delete()
        sharer = User.objects.create(open_id="test sharer",
                                     name="test sharer",
                                     head="head")
        shared = User.objects.create(open_id="test shared",
                                     name="test shared",
                                     head="head")
        shared.save()
        sharer.save()

    def test_add_share_id_lost(self):
        '''
        This is a unittest for add_share
        error: id lost
        '''
        payload = {}
        response = self.client.post('/api/share/add',
                                    data=payload,
                                    content_type="application/json")
        self.assertEqual(400, response.json()['code'])

    def test_add_share(self):
        '''
        This is a unittest for add_share
        error: none
        '''
        time = datetime(2021, 3, 4, 11, 12, 13)
        payload = {
            'sharer_open_id': "test sharer",
            'shared_open_id': "test shared",
            'timestamp': app.times.datetime2timestamp(time)
        }
        response = self.client.post('/api/share/add',
                                    data=payload,
                                    content_type="application/json")
        self.assertEqual(200, response.json()['code'])
        timestamp = app.times.datetime2timestamp(time)
        expected_result = "test shared" + '&' + str(timestamp) + "_&_"
        sharer = User.objects.get(open_id="test sharer")
        shared = User.objects.get(open_id="test shared")
        self.assertEqual(sharer.auth_user, expected_result)
        expected_result = "test sharer" + '&' + str(timestamp) + "_&_"
        self.assertEqual(shared.authed_user, expected_result)

    def test_delete_share_id_lost(self):
        '''
        This is a unittest for delete_share
        error: id lost
        '''
        payload = {'open_id': "test"}
        response = self.client.post('/api/share/delete',
                                    data=payload,
                                    content_type="application/json")
        self.assertEqual(400, response.json()['code'])

    def test_delete_share(self):
        '''
        This is a unittest for delete_share
        error: none
        '''
        payload = {
            'sharer_open_id': "test sharer",
            'shared_open_id': "test shared"
        }
        response = self.client.post('/api/share/delete',
                                    data=payload,
                                    content_type="application/json")
        sharer = User.objects.get(open_id="test sharer")
        shared = User.objects.get(open_id="test shared")
        self.assertEqual(200, response.json()['code'])
        self.assertEqual("", shared.authed_user)
        self.assertEqual("", sharer.auth_user)

    def test_get_my_sharing_user_openid_lost(self):
        '''
        This is a unittest for get_my_sharing_user
        error: openid lost
        '''
        payload = {}
        response = self.client.get('/api/share/sharing',
                                   data=payload,
                                   content_type="application/json")
        self.assertEqual(400, response.json()['code'])

    def test_get_my_sharing_user(self):
        '''
        This is a unittest for get_my_sharing_user
        error: none
        '''
        payload = {'open_id': "test sharer"}
        time = datetime(2021, 3, 5, 11, 12, 13)
        timestamp = app.times.datetime2timestamp(time)
        sharer = User.objects.get(open_id="test sharer")
        sharer.auth_user = "test shared" + '&' + str(timestamp) + "_&_"
        sharer.save()
        response = self.client.get('/api/share/sharing',
                                   data=payload,
                                   content_type="application/json")
        self.assertEqual(200, response.json()['code'])
        expected_result = [{
            'open_id': "test shared",
            'name': "test shared",
            'head': "head",
            'timestamp': str(app.times.datetime2timestamp(time))
        }]
        self.assertEqual(expected_result,
                         response.json()['data']['sharing_list'])

    def test_get_user_share_to_me_openid_lost(self):
        '''
        This is a unittest for get_user_share_to_me
        error: openid lost
        '''
        payload = {}
        response = self.client.get('/api/share/shared',
                                   data=payload,
                                   content_type="application/json")
        self.assertEqual(400, response.json()['code'])

    def test_get_user_share_to_me(self):
        '''
        This is a unittest for get_user_share_to_me
        error: none
        '''
        payload = {'open_id': "test shared"}
        shared = User.objects.get(open_id="test shared")
        time = datetime(2021, 3, 5, 11, 12, 13)
        timestamp = app.times.datetime2timestamp(time)
        shared.authed_user = "test sharer" + '&' + str(timestamp) + "_&_"
        shared.save()
        response = self.client.get('/api/share/shared',
                                   data=payload,
                                   content_type="application/json")
        self.assertEqual(200, response.json()['code'])
        expected_result = [{
            'open_id': "test sharer",
            'name': "test sharer",
            'head': "head",
            'timestamp': str(app.times.datetime2timestamp(time))
        }]
        self.assertEqual(expected_result,
                         response.json()['data']['shared_list'])

    def test_get_user_by_name_name_lost(self):
        """
        this is a test for get_user_by_name
        error: name lost
        """
        payload = {}
        response = self.client.get('/api/share/find',
                                   data=payload,
                                   content_type="application/json")
        self.assertEqual(400, response.json()['code'])

    def test_get_my_sharing_user_none(self):
        '''
        This is a unittest for get_my_sharing_user
        error: none result: none
        '''
        payload = {'open_id': "test sharer"}
        response = self.client.get('/api/share/sharing',
                                   data=payload,
                                   content_type="application/json")
        self.assertEqual(200, response.json()['code'])
        self.assertEqual([], response.json()['data']['sharing_list'])

    def test_get_user_share_to_me_none(self):
        '''
        This is a unittest for get_user_share_to_me
        error: none result: none
        '''
        payload = {'open_id': "test shared"}
        response = self.client.get('/api/share/shared',
                                   data=payload,
                                   content_type="application/json")
        self.assertEqual(200, response.json()['code'])
        self.assertEqual([], response.json()['data']['shared_list'])

    def test_get_user_by_name_noexist(self):
        """
        this is a test for get_user_by_name
        error: none  name:not exist
        """
        new_user = User.objects.create(
            open_id="test user",
            name="test user",
            head="test head",
            city="beijing",
        )
        new_user.save()
        payload = {
            'open_id': "test sharer",
            'exp_name': "test user"
        }
        expected_user = [{
            'open_id': "test user",
            'name': "test user",
            'head': "test head",
            'city': "beijing",
            'fan': 0,
            'video_count': 0
        }]
        response = self.client.get('/api/share/find',
                                   data=payload,
                                   content_type="application/json")
        self.assertEqual(200, response.json()['code'])
        self.assertEqual(expected_user, response.json()['data']['exp_list'])
        User.objects.filter(open_id="test user").delete()

    def test_get_user_by_name_exist(self):
        """
        this is a test for get_user_by_name
        error: none  name:exist
        """
        sharer = User.objects.get(open_id="test sharer")
        sharer.auth_user = "test user"
        sharer.save()
        payload = {
            'open_id': "test sharer",
            'exp_name': "test user"
        }
        expected_user = []
        response = self.client.get('/api/share/find',
                                   data=payload,
                                   content_type="application/json")
        self.assertEqual(200, response.json()['code'])
        self.assertEqual(expected_user, response.json()['data']['exp_list'])
        sharer.auth_user = ""
        sharer.save()

    def tearDown(self):
        """
        this is the deconstruction for share module
        """
        User.objects.filter(open_id="test sharer").delete()
        User.objects.filter(open_id="test shared").delete()
