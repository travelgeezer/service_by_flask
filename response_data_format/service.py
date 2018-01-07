# -*- coding: utf-8 -*-

import json
import base64
from flask import Blueprint, request
from user.utils import decrypt_rsa, private_key

response_data_format = Blueprint('response_data_format', __name__)

@response_data_format.route('/api/v1/response_data_format/<data>')
def data_format(data):

    data = {
        "code": 200,
        "data": data,
        "info": "success"
    }

    return json.dumps(data)


@response_data_format.route('/api/v1/test_rsa/', methods=['POST'])
def test_rsa():
    data = request.get_json()
    key = data.get('key')
    print(key)
    cipher = decrypt_rsa(private_key, base64.b64decode(key))
    print('cipher: ', cipher)

    data = {
        "code": 200,
        "data": cipher,
        "info": "success"
    }

    return json.dumps(data)
