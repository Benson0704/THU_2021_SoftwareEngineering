'''
this module provides necessary functions and auxiliary functions
WARNING:
all fucntions not used to handle frontend request DIRECTLY should write here
'''
from app.models import User
from app.models import Video


def create_user(open_id, video_list, count_dictionary):
    '''
    this function should create a user in User model
    untest: 3.24
    '''
    new_user = User(_open_id=open_id,
                    _public_count=count_dictionary['public_count'],
                    _friend_count=count_dictionary['friend_count'],
                    _private_count=count_dictionary['private_count'],
                    _all_count=count_dictionary['all_count'])
    new_user.save()
