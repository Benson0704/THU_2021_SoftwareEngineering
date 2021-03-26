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
STANDARD_DATE = "%Y-%m-%d %H:%M:%S"


def datetime2string(_datetime):
    '''
    receive: a datetime.datetime object
    return: a string like yyyy-mm-dd hh:mm:ss
    '''
    os.environ['TZ'] = 'UTC'
    return _datetime.strftime(STANDARD_DATE)


def datetime2timestamp(_datetime):
    '''
    receive: a datetime.datetime object
    return: timestamp length=10
    '''
    os.environ['TZ'] = 'UTC'
    return time.mktime(
        time.strptime(_datetime.strftime(STANDARD_DATE), STANDARD_DATE))


def string2timestamp(_string):
    '''
    receive: a string like yyyy-mm-dd hh:mm:ss
    return: timestamp length=10
    '''
    os.environ['TZ'] = 'UTC'
    return time.mktime(time.strptime(_string, STANDARD_DATE))


def string2datetime(_string):
    '''
    receive: a string like yyyy-mm-dd hh:mm:ss
    return: a datetime.datetime object
    '''
    os.environ['TZ'] = 'UTC'
    return datetime.datetime.strptime(_string, STANDARD_DATE)


def timestamp2datetime(_timestamp):
    '''
    receive: timestamp length=10
    return: a datetime.datetime object
    '''
    os.environ['TZ'] = 'UTC'
    while _timestamp > 9999999999:
        _timestamp = _timestamp // 10
    return datetime.datetime.strptime(
        time.strftime(STANDARD_DATE, time.localtime(_timestamp)),
        STANDARD_DATE)


def timestamp2string(_timestamp):
    '''
    receive: timestamp length=10
    return: a string like yyyy-mm-dd hh:mm:ss
    '''
    os.environ['TZ'] = 'UTC'
    while _timestamp > 9999999999:
        _timestamp = _timestamp // 10
    return time.strftime(STANDARD_DATE, time.localtime(_timestamp))
