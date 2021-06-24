from flask import Blueprint


receitas = Blueprint('receitas', __name__, url_prefix='/receitas')
categorias = Blueprint('categorias', __name__, url_prefix='/categorias')
ingredientes = Blueprint('ingredientes', __name__, url_prefix='/ingredientes')
unidades_medida = Blueprint('unidades_medida', __name__,
                            url_prefix='/unidades-de-medida')

# Registra blueprints como subrotas
receitas.register_blueprint(categorias)
receitas.register_blueprint(ingredientes)
ingredientes.register_blueprint(unidades_medida)
