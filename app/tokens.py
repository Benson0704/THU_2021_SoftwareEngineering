'''
this module provides functions for encryption:
    all variables and return values are STRING

METHOD: AES.ECB
        KEY length=32
'''
import base64
from Crypto.Cipher import AES
KEY = 'FullHouse=WbnYzxZxyLwkGr'


def encode(string):
    '''
    this function encrypts strings by using AES
    receive: a string needed encryption
    return: a string encrypted
    '''
    while len(string) % 48 != 0:  # AES need mod16=0, base64 need mod3=0
        string += '\0'
    return base64.encodebytes(AES.new(
        KEY, AES.MODE_ECB).encrypt(string)).decode('utf-8')


def decode(code):
    '''
    this function decrypts strings by using AES
    receive: a string needed decryption
    return: a string decrypted
    '''
    return AES.new(KEY, AES.MODE_ECB).decrypt(
        base64.decodebytes(
            code.encode('utf-8'))).decode('utf-8').split('\0')[0]
