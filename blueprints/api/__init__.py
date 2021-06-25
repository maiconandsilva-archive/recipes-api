from flask.blueprints import Blueprint

from .receitas.endpoints import *


bp_api = Blueprint('api', __name__)

bp_api.register_blueprint(bp_receitas)

