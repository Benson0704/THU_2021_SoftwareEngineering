'''
this file should be a .py file as tests for login
'''

import sys
import os
sys.path.append('..')
os.environ['DJANGO_SETTINGS_MODULE'] = 'app.settings'
import django
django.setup()
from logIn.tests import test_logIn


def test():
    test_logIn()
