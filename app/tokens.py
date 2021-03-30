'''
this module provides functions for encryption:
    all variables and return values are STRING

METHOD: AES.ECB
        KEY length=32
'''
import base64
from Crypto.Cipher import AES
KEY = 'FullHouse=WbnYzxZxyLwkGr'


def encode_token(string):
    '''
    this function encrypts strings by using AES
    receive: a string needed encryption
    return: a string encrypted
    '''
    while len(string) % 16 != 0:  # AES need mod16=0, base64 need mod4=0
        string += '\0'
    string = AES.new(KEY, AES.MODE_ECB).encrypt(string)
    string = base64.encodebytes(string).decode('utf-8')
    while len(string) % 3 != 0:
        string += '='
    return string


def decode_token(code):
    '''
    this function decrypts strings by using AES
    receive: a string needed decryption
    return: a string decrypted
    '''
    return AES.new(KEY, AES.MODE_ECB).decrypt(
        base64.decodebytes(
            code.encode('utf-8'))).decode('utf-8').split('\0')[0]
