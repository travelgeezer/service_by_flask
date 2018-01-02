# -*- coding: utf-8 -*-

import json
from datetime import datetime

from flask import Blueprint, request
from flask_mongoengine.wtf import model_form
from .models import User


UserForm = model_form(User)

user = Blueprint('user', __name__)

@user.route('/api/v1/register', methods=['POST'])
def register():

    data = request.get_json()
    user_name = data.get('name')
    user_account = data.get('account')
    user_password = data.get('password')

    if not user_name or not user_account or not user_password:
        return 'Missing parameters'

    try:
        User.objects.get(user_account__nin=user_account)
        return 'user exist'
    except User.DoesNotExist:
        pass

    u = User(user_name=user_name,
             user_account=user_account,
             user_password=User.encryption(user_password),
             create_by=user_name,
             create_time= datetime.now(),
             update_by=user_name,
             update_time=datetime.now())
    u.save()

    return 'name: {}, account: {}, password: {}'.format(user_name, user_account, user_password)



@user.route('/api/v1/user', methods=['POST'])
def user_info():
    data = request.get_json()

    try:
        user = User.objects.get(user_account=data.get('account'))
        return json.dumps(user.json)
    except User.DoesNotExist:
        return 'Not found user'


@user.route('/api/v1/users')
def users():
    users  = User.objects.all()
    result = [o.json for o in users]
    return json.dumps(result)
