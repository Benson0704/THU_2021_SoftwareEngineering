'''
this file should be a .py file as tests for login function
'''
import unittest
from datetime import datetime
import app.utils
import app.times
from app.models import User, Video
import pytest


@pytest.mark.django_db
class TestLogin(unittest.TestCase):
    '''
    This is a unittest for logIn
    '''
    def setUp(self):
        # User.objects.all().delete()
        # Video.objects.all().delete()  # this two lines only for test
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
            create_time='2021-03-07 12:13:14',
            like_count=10,
            comment_count=5,
            view_count=20,
            pending=False)
        new_video.save()
        Video.objects.filter(photo_id='this is a photo on Mars').delete()
        new_video = Video.objects.create(user=brisa,
                                         photo_id="this is a photo on Mars",
                                         caption="Mars view🔥",
                                         cover="https://MarsView",
                                         play_url="https://PlayMarsView",
                                         create_time='2021-03-07 12:13:14',
                                         like_count=10,
                                         comment_count=5,
                                         view_count=20,
                                         pending=False)
        new_video.save()

    def test_initialize_new_user(self):
        '''
        this is a test for initialize_registered_user
        '''
        open_id = "Test open_id"
        video_list = []
        video = {
            'photo_id': "Test photo_id",
            'caption': "Test caption",
            'cover': "https://TestCover",
            'play_url': "https://TestPlayUrl",
            'create_time': 1203011101010,
            'like_count': 10,
            'comment_count': 5,
            'view_count': 20,
            'pending': False
        }
        video_list.append(video)
        count_dictionary = {
            'public_count': 1,
            'friend_count': 0,
            'private_count': 0,
            'all_count': 1
        }
        user_data = {
            'name': "new user",
            'sex': 'M',
            'head': "https://ThisIsAHandsomeMan",
            'bigHead': "",
            'city': "Chengdu",
            'fan': 20,
            'follow': 20,
        }

        app.utils.initialize_new_user(open_id=open_id,
                                      user_data=user_data,
                                      video_list=video_list,
                                      count_dictionary=count_dictionary)
        self.assertTrue(User.objects.filter(open_id=open_id).exists())
        self.assertTrue(
            Video.objects.filter(photo_id="Test photo_id").exists())

    def test_get_registered_user(self):
        '''
        this is a test for get_registered_user
        '''
        res_video_list, res_count_dictionary = app.utils.get_registered_user(
            "todayisagoodday")
        expected_video_list = [
            {
                'photo_id':
                "this is a sunset photo in Hogwards",
                'caption':
                "hogwards sunset",
                'cover':
                "https://HogwardsSunset",
                'play_url':
                "https://PlayHogwardsSunset",
                'create_time':
                app.times.datetime2timestamp(datetime(2021, 3, 7, 12, 13, 14)),
                'like_count':
                10,
                'comment_count':
                5,
                'view_count':
                20,
                'pending':
                False
            },
            {
                'photo_id':
                "this is a photo on Mars",
                'caption':
                "Mars view🔥",
                'cover':
                "https://MarsView",
                'play_url':
                "https://PlayMarsView",
                'create_time':
                app.times.datetime2timestamp(datetime(2021, 3, 7, 12, 13, 14)),
                'like_count':
                10,
                'comment_count':
                5,
                'view_count':
                20,
                'pending':
                False
            },
        ]
        expected_count_dictionary = {
            'open_id': "todayisagoodday",
            'public_count': 2,
            'friend_count': 0,
            'private_count': 0,
            'video_count': 2,
            'name': "brisa",
            'sex': True,
            'head': "https://ThisIsABeautifulGirl",
            'bigHead': "",
            'city': "Shanghai",
            'fan': 20,
            'follow': 20,
        }
        self.assertEqual(res_video_list, expected_video_list)
        self.assertEqual(res_count_dictionary, expected_count_dictionary)

    def test_update_registered_user(self):
        '''
        this is a test for update_registered_user
        '''

        video_list = [{
            'photo_id': "this is a sunset photo in Hogwards",
            'caption': "hogwards sunset",
            'cover': "https://HogwardsSunset",
            'play_url': "https://PlayHogwardsSunset",
            'create_time': 0000000000000,
            'like_count': 10,
            'comment_count': 5,
            'view_count': 20,
            'pending': False
        }, {
            'photo_id': "this is a dog in New Zealand",
            'caption': "New Zealand dog",
            'cover': "https://NewZealanddog",
            'play_url': "https://PlayNewZealanddog",
            'create_time': 0000000000000,
            'like_count': 10,
            'comment_count': 5,
            'view_count': 20,
            'pending': False
        }]
        count_dictionary = {
            'public_count': 2,
            'friend_count': 0,
            'private_count': 0,
            'all_count': 2,
        }
        user_data = {
            'name': "brisa",
            'sex': 'F',
            'head': "https://ThisIsABeautifulGirl",
            'bigHead': "",
            'city': "Beijing",
            'fan': 20,
            'follow': 20,
        }
        app.utils.update_registered_user(open_id="todayisagoodday",
                                         user_data=user_data,
                                         video_list=video_list,
                                         count_dictionary=count_dictionary)
        self.assertFalse(
            Video.objects.filter(photo_id="this is a photo on Mars").exists())
        self.assertTrue(
            Video.objects.filter(
                photo_id="this is a dog in New Zealand").exists())
        user = User.objects.filter(open_id="todayisagoodday")
        self.assertEqual(user[0].city, "Beijing")

    def test_is_registered(self):
        '''
        this is a test for is_registered
        '''
        self.assertTrue(app.utils.is_registered("todayisagoodday"))

    def test_get_total_like_count(self):
        '''
        this is a test for get_total_like_count
        '''
        open_id = "todayisagoodday"
        self.assertEqual(app.utils.get_total_like_count(open_id), 20)

    def test_get_total_comment_count(self):
        '''
        this is a test for get_total_comment_count
        '''
        open_id = "todayisagoodday"
        self.assertEqual(app.utils.get_total_comment_count(open_id), 10)

    def test_get_total_view_count(self):
        '''
        this is a test for get_total_view_count
        '''
        open_id = "todayisagoodday"
        self.assertEqual(app.utils.get_total_view_count(open_id), 40)

    def test_store_token(self):
        '''
        this is a test for store_token
        '''
        open_id = "todayisagoodday"
        access_token = "abcdefghijklmn"
        refresh_token = "abcdefghijklmn"
        expected_token = "9XZzf6up5SH8U1JFUKs=\n"
        app.utils.store_token(open_id, access_token, refresh_token)
        user = User.objects.filter(open_id=open_id)
        self.assertEqual(user[0].access_token, expected_token)
        self.assertEqual(user[0].refresh_token, expected_token)

    def test_get_token(self):
        '''
        this is a test for get_token
        '''
        open_id = "todayisagoodday"
        access_token, refresh_token = app.utils.get_token(open_id)
        expected_token = "abcdefghijklmn"
        self.assertEqual(access_token, expected_token)
        self.assertEqual(refresh_token, expected_token)

    def test_encoding(self):
        '''
        this is a test for encoding
        '''
        message = {
            "name": "brisa"
        }
        coding = app.utils.encoding(message)
        expected_coding = (
            "eyJ0eXAiOiJKV1QiLCJhbGci"
            "OiJIUzI1NiJ9.eyJuYW1lIjoiYnJpc2EifQ.IWgS8bm"
            "QRY0JBiqz3IFrqq7-0LjJ7JIYFivfZ8prMK0"
        )
        self.assertEqual(coding, expected_coding)

    def tearDown(self):
        User.objects.filter(open_id="todayisagoodday").delete()
        new_user = User.objects.filter(open_id="Test open_id")
        if new_user:
            new_user.delete()


if __name__ == '__main__':

    unittest.main()
