# -*- coding: utf-8 -*-

import json
from flask import Blueprint, request


response_data_format = Blueprint('response_data_format', __name__)

@response_data_format.route('/api/v1/response_data_format/<data>')
def data_format(data):
    data = {
        "code": 0,
        "data": data,
        "info": "success"
    }

    return json.dumps(data)
