from flask.blueprints import Blueprint

from .receitas.endpoints import *
from .usuarios.blueprint import *
from .usuarios.endpoints import *


bp_api = Blueprint('api', __name__)

bp_api.register_blueprint(bp_receitas)
bp_api.register_blueprint(bp_usuario)
