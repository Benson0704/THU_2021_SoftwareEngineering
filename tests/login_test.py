'''
this file should be a .py file as tests for login
'''
from login import utils
from app.models import User,Video
import unittest
from datetime import datetime


class TestLogin(unittest.TestCase):
    '''
    This is a unittest for User
    '''
    def setUp(self):
        brisa = User.objects.create(open_id="todayisagoodday",
                                    public_count=2,
                                    friend_count=0,
                                    private_count=0,
                                    all_count=2)
        brisa.save()

        new_video = Video.objects.create(user=brisa.open_id,
                                         photo_id="this is a sunset photo in Hogwards",
                                         caption="hogwards sunset",
                                         cover="https://HogwardsSunset",
                                         play_url="https://PlayHogwardsSunset",
                                         create_time=20210307191817,
                                         like_count=2021,
                                         comment_count=74,
                                         view_count=200074,
                                         pending=False)
        new_video.save()
        new_video = Video.objects.create(user=brisa.open_id,
                                         photo_id="this is a photo on Mars",
                                         caption="Mars view",
                                         cover="https://MarsView",
                                         play_url="https://PlayMarsView",
                                         create_time=20210307191817,
                                         like_count=2021,
                                         comment_count=74,
                                         view_count=200074,
                                         pending=False)
        new_video.save()


    def tearDown(self):
        User.objects.filter(open_id="todayisagoodday").delete()


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
        self.assertTrue(User.objects.filter(open_id=open_id).exists())
        self.assertTrue(Video.objects.filter(photo_id="Test photo_id").exists())


    def test_get_registered_user(self):
        res_video_list, res_count_dictionary = utils.get_registered_user("todayisagoodday")
        expected_video_list = [
            {
                'photo_id': "this is a sunset photo in Hogwards",
                'caption': "hogwards sunset",
                'cover': "https://HogwardsSunset",
                'play_url': "https://PlayHogwardsSunset",
                'create_time': 20210307191817,
                'like_count': 2021,
                'comment_count': 74,
                'view_count': 200074,
                'pending': False
            },
            {
                'photo_id': "this is a photo on Mars",
                'caption': "Mars view",
                'cover': "https://MarsView",
                'play_url': "https://PlayMarsView",
                'create_time': 20210307191817,
                'like_count': 2021,
                'comment_count': 74,
                'view_count': 200074,
                'pending': False
            },
        ]
        expected_count_dictionary = {
            'open_id' : "todayisagoodday",
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
                'photo_id': "this is a sunset photo in Hogwards",
                'caption': "hogwards sunset",
                'cover': "https://HogwardsSunset",
                'play_url': "https://PlayHogwardsSunset",
                'create_time': 20210307191817,
                'like_count': 2021,
                'comment_count': 74,
                'view_count': 200074,
                'pending': False
            },
            {
                'photo_id': "this is a dog in New Zealand",
                'caption': "New Zealand dog",
                'cover': "https://NewZealanddog",
                'play_url': "https://PlayNewZealanddog",
                'create_time': 20210307191817,
                'like_count': 2021,
                'comment_count': 74,
                'view_count': 200074,
                'pending': False
            }
        ]
        count_dictionary = {
            'public_count' : 2,
            'friend_count' : 0,
            'private_count' : 0,
            'all_count' : 2
        }
        utils.update_registered_user(open_id="todayisagoodday", video_list=video_list, count_dictionary=count_dictionary)
        self.assertFalse(Video.objects.filter(photo_id="this is a photo on Mars").exists())
        self.assertTrue(Video.objects.filter(photo_id="this is a dog in New Zealand").exists())


    def test_is_registered(self):
        self.assertTrue(utils.is_registered("todayisagoodday"))


def test():
    unittest.main()
    

if __name__ == '__main__':
    unittest.main()