# -*- coding: utf-8 -*-

from service_by_flask.app import app
from user.service import user
from response_data_format.service import response_data_format

app.register_blueprint(user)
app.register_blueprint(response_data_format)
