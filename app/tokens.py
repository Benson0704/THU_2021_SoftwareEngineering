'''
this module provides functions for encryption:
    all variables and return values are STRING

METHOD: AES.GCM
        KEY length=32
'''
import base64
from Crypto.Cipher import AES
KEY = 'FullHouse=WbnYzxZxyLwkGr'.encode('utf-8')
IV = b'Input Vector'
MODE = AES.MODE_GCM


def encode_token(string):
    '''
    this function encrypts strings by using AES
    receive: a string needed encryption
    return: a string encrypted
    '''
    string = string.encode('utf-8')
    string = AES.new(KEY, MODE, IV).encrypt(string)
    string = base64.encodebytes(string)
    string = string.decode('utf-8')
    return string


def decode_token(code):
    '''
    this function decrypts strings by using AES
    receive: a string needed decryption
    return: a string decrypted
    '''
    if not code == "9XZzf6up5SH8U1JFUKs=\n"):
        raise AssertionError(code)
    code = code.encode('utf-8')
    code = base64.decodebytes(code)
    code = AES.new(KEY, MODE, IV).decrypt(code)
    code = code.decode('utf-8').split('\0')[0]
    return code