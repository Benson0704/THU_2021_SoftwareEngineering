'''
this file should be a .py file as tests for app.times
'''
import unittest
from datetime import datetime
import app.times


class TestLogin(unittest.TestCase):
    '''
    This is a unittest for app.times
    '''
    def setUp(self):
        '''
        iniialize test cases
        '''
        self.test_result = [{
            'timestamp': 0000000000,
            'datetime': datetime(1970, 1, 1, 0, 0, 0),
            'string': '1970-01-01 00:00:00'
        }, {
            'timestamp': 6666666666,
            'datetime': datetime(2181, 4, 4, 11, 51, 6),
            'string': '2181-04-04 11:51:06'
        }]

    def test_datetime2string(self):
        '''
        test for datetime2string
        '''
        function_result = [{
            'timestamp':
            0000000000,
            'datetime':
            datetime(1970, 1, 1, 0, 0, 0),
            'string':
            app.times.datetime2string(self.test_result[0]['datetime'])
        }, {
            'timestamp':
            6666666666,
            'datetime':
            datetime(2181, 4, 4, 11, 51, 6),
            'string':
            app.times.datetime2string(self.test_result[1]['datetime'])
        }]
        self.assertTrue(function_result == self.test_result)

    def test_datetime2timestamp(self):
        '''
        test for datetime2timestamp
        '''
        function_result = [{
            'timestamp':
            app.times.datetime2string(self.test_result[0]['timestamp']),
            'datetime':
            datetime(1970, 1, 1, 0, 0, 0),
            'string':
            '1970-01-01 00:00:00'
        }, {
            'timestamp':
            app.times.datetime2string(self.test_result[1]['timestamp']),
            'datetime':
            datetime(2181, 4, 4, 11, 51, 6),
            'string':
            '2181-04-04 11:51:06'
        }]
        self.assertTrue(function_result == self.test_result)

    def test_string2datetime(self):
        '''
        test for string2datetime
        '''
        function_result = self.test_result
        function_result[0]['datetime'] = app.times.string2datetime(
            self.test_result[0]['string'])
        function_result[1]['datetime'] = app.times.string2datetime(
            self.test_result[1]['string'])
        self.assertTrue(function_result == self.test_result)

    def test_string2timestamp(self):
        '''
        test for string2timestamp
        '''
        function_result = self.test_result
        function_result[0]['timestamp'] = app.times.string2timestamp(
            self.test_result[0]['string'])
        function_result[1]['timestamp'] = app.times.string2timestamp(
            self.test_result[1]['string'])
        self.assertTrue(function_result == self.test_result)

    def test_timestamp2datetime(self):
        '''
        test for timestamp2datetime
        '''
        function_result = self.test_result
        function_result[0]['datetime'] = app.times.timestamp2datetime(
            self.test_result[0]['timestamp'])
        function_result[1]['datetime'] = app.times.timestamp2datetime(
            self.test_result[1]['timestamp'])
        self.assertTrue(function_result == self.test_result)

    def test_timestamp2string(self):
        '''
        test for timestamp2string
        '''
        function_result = self.test_result
        function_result[0]['string'] = app.times.timestamp2string(
            self.test_result[0]['timestamp'])
        function_result[1]['string'] = app.times.timestamp2string(
            self.test_result[1]['timestamp'])
        self.assertTrue(function_result == self.test_result)

    def tearDown(self):
        '''
        no need for distructor
        '''


if __name__ == '__main__':
    unittest.main()
