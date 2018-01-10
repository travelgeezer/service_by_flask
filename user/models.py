# -*- coding: utf-8 -*-

from service_by_flask.ext import db, bcrypt

class User(db.Document):
    user_name = db.StringField(max_length=256, required=True)
    user_account = db.StringField(max_length=256, required=True)
    user_password = db.StringField(max_length=256, required=True)
    create_by = db.StringField(max_length=256, required=True)
    create_time = db.DateTimeField(required=True)
    update_by = db.StringField(max_length=256, required=True)
    update_time = db.DateTimeField(required=True)

    @staticmethod
    def encryption(password):
        return bcrypt.generate_password_hash(password).decode('utf-8')

    def verify(self, password):
        return bcrypt.check_password_hash(self.user_password, password)

    @property
    def json(self):
        return {
            'name': self.user_name,
            'account': self.user_account
        }
