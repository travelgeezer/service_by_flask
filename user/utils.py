# -*- coding: utf-8 -*-
import os
from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA
from Crypto import Random
from Crypto.Cipher import AES

dir_path = os.path.dirname(__file__)
rsa_public_key_2048_path = os.path.join(dir_path, 'rsa_public_key_2048.pem')
pkcs8_rsa_private_key_2048_path = os.path.join(dir_path, 'pkcs8_rsa_private_key_2048.pem')

with open(rsa_public_key_2048_path, 'r') as f:
    pub = f.read()


with open(pkcs8_rsa_private_key_2048_path, 'r') as f:
    pri = f.read()

public_key = pub
private_key = pri

def encrypt(pub, message):
    ret = b''
    input_text = message[:128]
    while input_text:
        key =  RSA.importKey(pub)
        cipher = PKCS1_v1_5.new(key)
        ret += cipher.encrypt(input_text.encode(encoding='utf-8'))
        message = message[128:]
        input_text = message[:128]
    return ret

def decrypt(pri, cipher_text):
    key = RSA.importKey(pri)
    dsize = SHA.digest_size
    input_text = cipher_text[:256]
    ret = ''
    while input_text:
        sentinel = Random.new().read(15 + dsize)
        cipher = PKCS1_v1_5.new(key)
        _message = cipher.decrypt(cipher_text, sentinel)
        ret += _message.decode('utf-8')
        cipher_text = cipher_text[256:]
        input_text = cipher_text[:256]
    return ret


def test_crypt():
    msg = decrypt(pri, encrypt(pub, 'qqq123'))
    print(msg)
