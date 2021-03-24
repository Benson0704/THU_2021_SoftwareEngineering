'''
this file should be a .py file as tests for login
'''

import sys
import os
sys.path.append('..')
from logIn.tests import test_logIn


def test():
    test_logIn()


if __name__ == '__main__':
    test()