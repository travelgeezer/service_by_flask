# -*- coding: utf-8 -*-

import os
from flask import Flask
from .ext import db, bcrypt, CORS

def create_app():
    app = Flask(__name__)

    app.config.from_object('service_by_flask.config')

    db.init_app(app)

    bcrypt.init_app(app)

    CORS(app)

    return app
