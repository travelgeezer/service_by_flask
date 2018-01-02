# -*- coding: utf-8 -*-

from .factory import create_app

app = create_app()


@app.route('/')
def hello():
    return 'hello service by flask'
