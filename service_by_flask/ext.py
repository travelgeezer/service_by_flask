# -*- coding: utf-8 -*-

from flask_mongoengine import MongoEngine
from flask_bcrypt import Bcrypt
from flask_cors import CORS as cors

db = MongoEngine()
bcrypt = Bcrypt()
CORS = cors
