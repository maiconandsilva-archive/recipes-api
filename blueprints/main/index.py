from flask import request, current_app
from flask.json import jsonify
from flask.templating import render_template

from .blueprint import bp_main


@bp_main.route('/', defaults={'path': ''})
@bp_main.route('/<string:path>')
@bp_main.route('/<path:path>')
def index(path: str):
    current_app.logger.debug(path)
    return bp_main.send_static_file('dist/index.html')
