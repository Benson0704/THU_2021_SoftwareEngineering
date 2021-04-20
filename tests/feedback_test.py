'''
this file should be a .py file as tests for feedback module
'''
from django.test import TestCase
from app.models import 
import app.times
import pytest
from datetime import datetime


@pytest.mark.django_db
class TestAppTimes(unittest.TestCase):
    '''
    This is a unittest for feedback module
    '''
    def setUp(self):
        """
        this is the constructin of tests for analyse works
        """
        