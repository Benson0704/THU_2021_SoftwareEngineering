'''
this file should be a .py file as tests for share module
finish: 4.22
'''
from django.test import TestCase
from app.models import User
import pytest


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
        payload = {
            'sharer_open_id': "test sharer",
            'shared_open_id': "test shared"
        }
        response = self.client.post('/api/share/add',
                                    data=payload,
                                    content_type="application/json")
        self.assertEqual(200, response.json()['code'])
        expected_result = "test shared_&_"
        sharer = User.objects.get(open_id="test sharer")
        shared = User.objects.get(open_id="test shared")
        self.assertEqual(sharer.auth_user, expected_result)
        expected_result = "test sharer_&_"
        self.assertEqual(shared.authed_user, expected_result)

    def test_delete_share_id_lost(self):
        '''
        This is a unittest for delete_share
        error: id lost
        '''
        payload = {
            'open_id': "test"
        }
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
        payload = {
            'open_id': "test sharer"
        }
        sharer = User.objects.get(open_id="test sharer")
        sharer.auth_user = "test shared_&_"
        sharer.save()
        response = self.client.get('/api/share/sharing',
                                   data=payload,
                                   content_type="application/json")
        self.assertEqual(200, response.json()['code'])
        expected_result = [{
            'open_id': "test shared",
            'name': "test shared",
            'head': "head"
        }]
        self.assertEqual(expected_result,
                         response.json()['data']['data']['sharing_list'])

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
        payload = {
            'open_id': "test shared"
        }
        shared = User.objects.get(open_id="test shared")
        shared.authed_user = "test sharer_&_"
        shared.save()
        response = self.client.get('/api/share/shared',
                                   data=payload,
                                   content_type="application/json")
        self.assertEqual(200, response.json()['code'])
        expected_result = [{
            'open_id': "test sharer",
            'name': "test sharer",
            'head': "head"
        }]
        self.assertEqual(expected_result,
                         response.json()['data']['data']['shared_list'])

    def tearDown(self):
        """
        this is the deconstruction for share module
        """
        User.objects.filter(open_id="test sharer").delete()
        User.objects.filter(open_id="test shared").delete()
