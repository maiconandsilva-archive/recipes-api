from flask.blueprints import Blueprint

from .receitas.endpoints import *


api = Blueprint('api', __name__)

api.register_blueprint(receitas)
