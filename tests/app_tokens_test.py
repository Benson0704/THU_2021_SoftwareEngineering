'''
this file should be a .py file as tests for app.tokens
'''
import unittest
import app.tokens


class TestAppTimes(unittest.TestCase):
    '''
    This is a unittest for app.times
    '''
    def setUp(self):
        '''
        iniialize test cases
        '''
        self.test_result = [
            'test', '1@_Test{,?}', '0123456789012345678901234567890123456789'
        ]

    def test_Cryption(self):
        output = []
        for i in self.test_result:
            output.append(app.tokens.decode(app.tokens.encode(i)))
        self.assertEqual(output, self.test_result)

    def tearDown(self):
        '''
        no need for distructor
        '''


if __name__ == '__main__':
    unittest.main()
