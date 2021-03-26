'''
this module meanly contains 6 functions for:
    datetime-string-timestamp(length=10) transfrom

Mention: django.models.dateTimeField is a datetime.datetime object

WARNING:
    all timestamps and datetimes are based on UTC
'''
import time
import datetime
import os


def datetime2string(_datetime):
    '''
    receive: a datetime.datetime object
    return: a string like yyyy-mm-dd hh:mm:ss
    '''
    os.environ['TZ'] = 'UTC'
    return _datetime.strftime("%Y-%m-%d %H:%M:%S")


def datetime2timestamp(_datetime):
    '''
    receive: a datetime.datetime object
    return: timestamp length=10
    '''
    os.environ['TZ'] = 'UTC'
    return time.mktime(
        time.strptime(_datetime.strftime("%Y-%m-%d %H:%M:%S"),
                      '%Y-%m-%d %H:%M:%S'))


def string2timestamp(_string):
    '''
    receive: a string like yyyy-mm-dd hh:mm:ss
    return: timestamp length=10
    '''
    os.environ['TZ'] = 'UTC'
    return time.mktime(time.strptime(_string, '%Y-%m-%d %H:%M:%S'))


def string2datetime(_string):
    '''
    receive: a string like yyyy-mm-dd hh:mm:ss
    return: a datetime.datetime object
    '''
    os.environ['TZ'] = 'UTC'
    return datetime.datetime.strptime(_string, '%Y-%m-%d %H:%M:%S')


def timestamp2datetime(_timestamp):
    '''
    receive: timestamp length=10
    return: a datetime.datetime object
    '''
    os.environ['TZ'] = 'UTC'
    while _timestamp > 9999999999:
        _timestamp = _timestamp // 10
    return datetime.datetime.strptime(
        time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(_timestamp)),
        '%Y-%m-%d %H:%M:%S')


def timestamp2string(_timestamp):
    '''
    receive: timestamp length=10
    return: a string like yyyy-mm-dd hh:mm:ss
    '''
    os.environ['TZ'] = 'UTC'
    while _timestamp > 9999999999:
        _timestamp = _timestamp // 10
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(_timestamp))


if __name__ == '__main__':  # test
    print(datetime2timestamp(datetime.datetime(1970, 1, 1, 0, 0, 0)))
    print(datetime2string(datetime.datetime(1970, 1, 1, 0, 0, 0)))
    print(string2datetime("1970-01-01 00:00:00"))
    print(string2timestamp("1970-01-01 00:00:00"))
    print(timestamp2datetime(00000000000))
    print(timestamp2string(0000000000))
