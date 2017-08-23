#-*- coding:utf-8 -*-
from Crypto.Cipher import AES
import urllib
import base64
import requests
import json


second_param = "010001"
third_param = "00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7"
forth_param = "0CoJUm6Qyw8W8jud"
    
def get_params( first_param):
    iv = "0102030405060708"
    first_key = forth_param
    second_key = 16 * 'a'
    h_encText = AES_encrypt(first_param, first_key, iv)
    h_encText = AES_encrypt(h_encText, second_key, iv)
    return h_encText

def AES_encrypt(text, key, iv):
    pad = 16 - len(text) % 16
    text = text + pad * chr(pad)
    encryptor = AES.new(key, AES.MODE_CBC, iv)
    encrypt_text = encryptor.encrypt(text)
    encrypt_text = base64.b64encode(encrypt_text)
    return encrypt_text

def get_encSecKey():
    encSecKey = "d473b9eca232f1b4090dd606b0df86de318748dd2eec307e4ed4345030fc4ee30331e598f41d5a6f5befaab94630ea1a1eda7cfade84fbec1a907913d2e4d2c8744bc572b99a050075e075b4537f645ecfa994f95906c32818e076aeda6bdb906bfa0bb96c4cf4bc3ed6d9ab76cf08441153d9d85e1ea3d78fa8d9210d581cee"
    return encSecKey

def get_postData(first_param):
    return {
         "params": get_params(first_param),
         "encSecKey": get_encSecKey()
    }

if __name__ == "__main__":
    param = '{"rid":"R_SO_4_405343230","offset":"0","total":"true","limit":"100","csrf_token":""}'
    pair = get_postData(param)
    print urllib.urlencode(pair)

    
