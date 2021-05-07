'''
this file should be a .py file as tests for login function
'''
import pytest
import unittest
from datetime import datetime
import app.utils
import app.times
from app.models import User, Video


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
        User.objects.filter(open_id="I am invisible").delete()
        temp = User.objects.create(open_id="I am invisible",
                                   name="temp",
                                   identity=True)
        temp.save()
        Video.objects.filter(
            photo_id='this is a sunset photo in Hogwards').delete()
        new_video = Video.objects.create(
            user=brisa,
            photo_id="this is a sunset photo in Hogwards",
            caption="hogwards sunset",
            cover="https://HogwardsSunset",
            play_url="https://PlayHogwardsSunset",
            create_time='2021-03-07 12:13:13',
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
                                         create_time='2021-03-07 12:13:15',
                                         like_count=10,
                                         comment_count=5,
                                         view_count=20,
                                         pending=False,
                                         labels="")
        new_video.save()

    def test_initialize_new_user(self):
        '''
        this is a test for initialize_registered_user
        '''
        open_id = "Male Test open_id"
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
            'name': "new male user",
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
        open_id = "Female Test open_id"
        user_data = {
            'name': "new female user",
            'sex': 'F',
            'head': "",
            'bigHead': "",
            'city': "Chengdu",
            'fan': 20,
            'follow': 20,
        }
        count_dictionary = {
            'public_count': 0,
            'friend_count': 0,
            'private_count': 0,
            'all_count': 0
        }
        app.utils.initialize_new_user(open_id=open_id,
                                      user_data=user_data,
                                      video_list=[],
                                      count_dictionary=count_dictionary)
        self.assertTrue(User.objects.filter(open_id=open_id).exists())
        user_data = {
            'name': "new user",
            'sex': '',
            'head': "",
            'bigHead': "",
            'city': "Chengdu",
            'fan': 20,
            'follow': 20,
        }
        open_id = "Test open_id"
        app.utils.initialize_new_user(open_id=open_id,
                                      user_data=user_data,
                                      video_list=[],
                                      count_dictionary=count_dictionary)
        self.assertTrue(User.objects.filter(open_id=open_id).exists())

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
                app.times.datetime2timestamp(datetime(2021, 3, 7, 12, 13, 13)),
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
                "Mars view",
                'cover':
                "https://MarsView",
                'play_url':
                "https://PlayMarsView",
                'create_time':
                app.times.datetime2timestamp(datetime(2021, 3, 7, 12, 13, 15)),
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
        time1 = datetime(2021, 3, 7, 12, 13, 13)
        time2 = datetime(2021, 3, 7, 12, 13, 15)
        video_list = [{
            'photo_id': "this is a sunset photo in Hogwards",
            'caption': "hogwards sunset",
            'cover': "https://HogwardsSunset",
            'play_url': "https://PlayHogwardsSunset",
            'create_time': app.times.datetime2timestamp(time1),
            'like_count': 10,
            'comment_count': 5,
            'view_count': 20,
            'pending': False
        }, {
            'photo_id': "this is a dog in New Zealand",
            'caption': "New Zealand dog",
            'cover': "https://NewZealanddog",
            'play_url': "https://PlayNewZealanddog",
            'create_time': app.times.datetime2timestamp(time2),
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
        user_data = {
            'name': "brisa",
            'sex': 'M',
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
        user = User.objects.filter(open_id="todayisagoodday")
        self.assertEqual(user[0].sex, 0)
        user_data = {
            'name': "brisa",
            'sex': '',
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
        user = User.objects.filter(open_id="todayisagoodday")
        self.assertEqual(user[0].sex, None)

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

    def test_get_videos_by_timestamp(self):
        """
        this is a test for get_videos_by_timestamp
        """
        open_id = "todayisagoodday"
        before_time = datetime(2021, 3, 7, 12, 13, 13)
        before_timestamp = app.times.datetime2timestamp(before_time)
        after_time = datetime(2021, 3, 7, 12, 13, 14)
        after_timestamp = app.times.datetime2timestamp(after_time)
        exp_results = Video.objects.filter(create_time="2021-03-07 12:13:13")
        results = app.utils.get_videos_by_timestamp(open_id, before_timestamp,
                                                    after_timestamp)
        self.assertEqual(exp_results[0].photo_id, results[0].photo_id)

    def test_get_all_open_id(self):
        """
        this is a test for get_all_open_id
        """
        open_id_list = app.utils.get_all_open_id()
        open_id = "todayisagoodday"
        self.assertTrue(open_id in open_id_list)

    def test_is_administrator_no(self):
        """
        this is a test for is_administrator, result: no
        """
        open_id = "todayisagoodday"
        re = app.utils.is_administrator(open_id=open_id)
        self.assertFalse(re)

    def test_is_administrator_yes(self):
        """
        this is a test for is_administrator, result: yes
        """
        open_id = "I am invisible"
        re = app.utils.is_administrator(open_id=open_id)
        self.assertTrue(re)

    def tearDown(self):
        User.objects.filter(open_id="todayisagoodday").delete()
        new_user = User.objects.filter(open_id="Test open_id")
        if new_user:
            new_user.delete()


if __name__ == '__main__':
    unittest.main()
