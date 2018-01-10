# -*- coding: utf-8 -*-

import json
import base64
from datetime import datetime
from .utils import decrypt_rsa, decrypt_aes, encrypt_aes, private_key, public_key
from flask import Blueprint, request
from flask_mongoengine.wtf import model_form
from .models import User

UserForm = model_form(User)

user = Blueprint('user', __name__)

@user.route('/api/v1/register/', methods=['POST'])
def register():
    data = request.get_json()
    key = data.get('key')
    user_name = data.get('name')
    user_account = data.get('account')
    user_password = data.get('password')

    response = {}
    aes_key = ''

    if not user_name or not user_account or not user_password:
        response['code'] = 2
        response['info'] = 'Missing parameters'
        return json.dumps(response)

    try:
        User.objects.get(user_account=user_account)
        info = encrypt_aes(aes_key, 'User exist')
        print(info)
        response['code'] = 2
        response['info'] = info.decode('utf-8')
        return json.dumps(response)
    except User.DoesNotExist:
        pass


    try:
        print(key)
        print(user_password)
        aes_key = decrypt_rsa(private_key, base64.b64decode(key))
        print('aes key:', aes_key)
        password = decrypt_aes(aes_key, user_password)
        print('passwrod:', password)
        print('key ---', aes_key)

        u = User(user_name=user_name,
                 user_account=user_account,
                 user_password=User.encryption(password),
                 create_by=user_name,
                 create_time= datetime.now(),
                 update_by=user_name,
                 update_time=datetime.now())
        u.save()

        response['code'] = 200
        response['data'] = u.json
        response['info'] = 'success'
        return json.dumps(response)

    except Exception as e:
        print(e)
        response['code'] = 2
        response['info'] = 'decrypt error'
        return json.dumps(response)

@user.route('/api/v1/login/', methods=['POST'])
def login():
    data = request.get_json()

    key = data.get('key')
    user_account = data.get('account')
    user_password = data.get('password')

    response = {}
    if not key or not user_account or not user_password:
        response['code'] = 2
        response['info'] = 'Missing parameters'

    try:
        user = User.objects.get(user_account=user_account)

        try:
            print('key: ', key)
            aes_key = decrypt_rsa(private_key, base64.b64decode(key))
            print('aes_key:', aes_key)
            print('password: ', user_password)
            password = decrypt_aes(aes_key, user_password)
            if user.verify(password):
                response['code'] = 200
                response['data'] = user.json
                response['info'] = 'login success!'
                return json.dumps(response)
            else:
                response['code'] = 2
                response['info'] = 'password error'
                return json.dumps(response)
        except Exception as e:
            print(e)
            response['code'] = 2
            response['info'] = 'decrypt error'
            return json.dumps(response)
    except User.DoseNotExist as e:
        print(e)
        response['code'] = 2
        response['info'] = 'User not exist'
        return json.dumps(response)


@user.route('/api/v1/user/', methods=['POST'])
def user_info():
    data = request.get_json()

    try:
        user = User.objects.get(user_account=data.get('account'))
        return json.dumps(user.json)
    except User.DoesNotExist:
        return 'Not found user'


@user.route('/api/v1/users/')
def users():
    users  = User.objects.all()
    result = [o.json for o in users]
    return json.dumps(result)
