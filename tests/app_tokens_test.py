'''
this file should be a .py file as tests for app.tokens
'''
import unittest
import app.tokens


class TestAppTokes(unittest.TestCase):
    '''
    This is a unittest for app.times
    '''
    def setUp(self):
        '''
        initialize test cases
        '''
        self.test_result = [
            'test', '1@_Test{,?}',
            '012345678901 2345678901 23456789012 3456789'
        ]

    def test_cryption(self):
        '''
        test for cryption
        '''
        output = []
        for i in self.test_result:
            output.append(app.tokens.decode_token(app.tokens.encode_token(i)))
        self.assertEqual(output, self.test_result)

    def tearDown(self):
        '''
        no need for distructor
        '''


if __name__ == '__main__':
    unittest.main()
