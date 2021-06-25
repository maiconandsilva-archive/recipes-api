from flask import Blueprint


bp_receitas = Blueprint('receitas', __name__, url_prefix='/receitas')
bp_categorias = Blueprint('categorias', __name__, url_prefix='/categorias')
bp_ingredientes = Blueprint('ingredientes', __name__, url_prefix='/ingredientes')
bp_unidades_medida = Blueprint('unidades_medida', __name__,
                               url_prefix='/unidades-de-medida')

# Registra blueprints como subrotas
bp_receitas.register_blueprint(bp_categorias)
bp_receitas.register_blueprint(bp_ingredientes)
bp_ingredientes.register_blueprint(bp_unidades_medida)
