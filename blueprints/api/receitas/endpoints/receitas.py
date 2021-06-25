from flask import abort
from typing import List

from blueprints.utils import requer_autenticacao
from models.receitas import Receita
from models.serialization import serialize
from ..blueprint import bp_receitas


@bp_receitas.route('/')
def listar():
    receita: List[Receita] = Receita.query.all()
    return serialize(receita)


@bp_receitas.route('/buscar/<busca>')
def buscar(busca: str):
    receita: Receita

    if not busca:
        return serialize([])

    receita = Receita.query.filter(
        Receita.nome.ilike('%{}%'.format(busca))).all()

    return serialize(receita)


@bp_receitas.route('/<int:receita_id>')
def buscar_por_id(receita_id: int):
    receita: Receita = Receita.query.get(receita_id)

    if receita is None:
        abort(404)

    return receita.serialize(ignore=lambda prop: prop[0] != 'email')
