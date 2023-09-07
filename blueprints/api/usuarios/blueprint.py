from flask import Blueprint


bp_usuario = Blueprint('usuario', __name__, url_prefix='/usuario')
bp_conta = Blueprint('conta', __name__, url_prefix='/conta')

# Registra blueprints como subrotas
bp_usuario.register_blueprint(bp_conta)
