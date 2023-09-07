from typing import List
from flask import abort

from blueprints.utils import requer_autenticacao
from models.receitas import IngredienteInfo
from models.serialization import serialize
from ..blueprint import bp_ingredientes


@bp_ingredientes.route('/')
def listar():
    ingrediente: List[IngredienteInfo] = IngredienteInfo.query.all()
    return serialize(ingrediente)


@bp_ingredientes.route('/<int:ingrediente_id>')
def buscar_por_id(ingrediente_id: int):
    ingrediente: IngredienteInfo = IngredienteInfo.query.get(ingrediente_id)

    if ingrediente is None:
        abort(404)

    return ingrediente.serialize()


@bp_ingredientes.route('/editar', methods=['POST'])
@requer_autenticacao
def editar():
    return 200


@bp_ingredientes.route('/criar', methods=['POST'])
@requer_autenticacao
def criar():
    pass


@bp_ingredientes.route('/excluir', methods=['POST'])
@requer_autenticacao
def deletar():
    pass
