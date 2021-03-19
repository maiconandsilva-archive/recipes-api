from flask import request

from ..main import main


@main.route('/')
def index():
    return '<h1>index</h1>'
