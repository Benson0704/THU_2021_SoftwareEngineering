'''
this file should be a .py file as tests for login
'''
import utils
from app.models import User,Video
import unittest
from datetime import datetime


class TestLogin(unittest.TestCase):
    '''
    This is a unittest for User
    '''
    def setUp(self):
        brisa = User.objects.create(_open_id="todayisagoodday",
                                    _public_count=2,
                                    _friend_count=0,
                                    _private_count=0,
                                    _all_count=2)
        brisa.save()

        new_video = Video.objects.create(_user=brisa,
                                         _photo_id="this is a sunset photo in Hogwards",
                                         _caption="hogwards sunset",
                                         _cover="https://HogwardsSunset",
                                         _play_url="https://PlayHogwardsSunset",
                                         _create_time=20210307191817,
                                         _like_count=2021,
                                         _comment_count=74,
                                         _view_count=200074,
                                         _pending=False)
        new_video.save()
        new_video = Video.objects.create(_user=brisa,
                                         _photo_id="this is a photo on Mars",
                                         _caption="Mars view",
                                         _cover="https://MarsView",
                                         _play_url="https://PlayMarsView",
                                         _create_time=20210307191817,
                                         _like_count=2021,
                                         _comment_count=74,
                                         _view_count=200074,
                                         _pending=False)
        new_video.save()


    def test_initialize_new_user(self):
        open_id = "Test open_id"
        video_list = []
        video = {
            'photo_id': "Test photo_id",
            'caption': "Test caption",
            'cover': "https://TestCover",
            'play_url': "https://TestPlayUrl",
            'create_time': 20210307191817,
            'like_count': 100,
            'comment_count': 100,
            'view_count': 1000,
            'pending': False
        }
        video_list.append(Video)
        count_dictionary = {
            'public_count' : 1,
            'friend_count' : 0,
            'private_count' : 0,
            'all_count' : 1
        }

        utils.initialize_new_user(open_id=open_id, video_list=video_list, count_dictionary=count_dictionary)
        self.assertTrue(User.objects.filter(_open_id=open_id).exists())
        self.assertTrue(Video.objects.filter(_photo_id="Test photo_id").exists())


    def test_get_registered_user(self):
        res_video_list, res_count_dictionary = utils.get_registered_user("todayisagoodday")
        expected_video_list = [
            {
                '_photo_id': "this is a sunset photo in Hogwards",
                '_caption': "hogwards sunset",
                '_cover': "https://HogwardsSunset",
                '_play_url': "https://PlayHogwardsSunset",
                '_create_time': 20210307191817,
                '_like_count': 2021,
                '_comment_count': 74,
                '_view_count': 200074,
                '_pending': False
            },
            {
                '_photo_id': "this is a photo on Mars",
                '_caption': "Mars view",
                '_cover': "https://MarsView",
                '_play_url': "https://PlayMarsView",
                '_create_time': 20210307191817,
                '_like_count': 2021,
                '_comment_count': 74,
                '_view_count': 200074,
                '_pending': False
            },
        ]
        expected_count_dictionary = {
            'public_count' : 2,
            'friend_count' : 0,
            'private_count' : 0,
            'all_count' : 2
        }
        self.assertEqual(res_video_list, expected_video_list)
        self.assertEqual(res_count_dictionary, expected_count_dictionary)

    
    def test_update_registered_user(self):
        open_id = "todayisagoodday"
        video_list = [
            {
                '_photo_id': "this is a sunset photo in Hogwards",
                '_caption': "hogwards sunset",
                '_cover': "https://HogwardsSunset",
                '_play_url': "https://PlayHogwardsSunset",
                '_create_time': 20210307191817,
                '_like_count': 2021,
                '_comment_count': 74,
                '_view_count': 200074,
                '_pending': False
            },
            {
                '_photo_id': "this is a dog in New Zealand",
                '_caption': "New Zealand dog",
                '_cover': "https://NewZealanddog",
                '_play_url': "https://PlayNewZealanddog",
                '_create_time': 20210307191817,
                '_like_count': 2021,
                '_comment_count': 74,
                '_view_count': 200074,
                '_pending': False
            }
        ]
        count_dictionary = {
            'public_count' : 2,
            'friend_count' : 0,
            'private_count' : 0,
            'all_count' : 2
        }
        utils.update_registered_user(open_id="todayisagoodday", video_list=video_list, count_dictionary=count_dictionary)
        self.assertFalse(Video.objects.filter(_photo_id="this is a photo on Mars").exists())
        self.assertTrue(Video.objects.filter(_photo_id="this is a dog in New Zealand").exists())


    def tearDown(self):
        User.objects.filter(_open_id="todayisagoodday").delete()



if __name__ == '__main__':
    unittest.main()