from flask import abort

from blueprints.utils import requer_autenticacao
from models.receitas import IngredienteInfo
from models.serialization import serialize
from ..blueprint import ingredientes


@ingredientes.route('/')
def listar():
    ingrediente: IngredienteInfo = IngredienteInfo.query.all()
    return serialize(ingrediente)


@ingredientes.route('/<int:ingrediente_id>')
def buscar_por_id(ingrediente_id):
    ingrediente: IngredienteInfo = IngredienteInfo.query.get(ingrediente_id)

    if ingrediente is None:
        abort(404)

    return ingrediente.serialize()

