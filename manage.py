# -*- coding: utf-8 -*-

from service_by_flask.app import app
from user.service import user

app.register_blueprint(user)
