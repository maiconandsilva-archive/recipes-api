from flask import abort

from blueprints.utils import requer_autenticacao
from models.receitas import Receita
from models.serialization import serialize
from ..blueprint import receitas


@receitas.route('/')
def listar():
    receita: Receita = Receita.query.all()
    return serialize(receita)


@receitas.route('/buscar/<busca>')
def buscar(busca: str):
    receita: Receita

    if not busca:
        return serialize([])

    receita = Receita.query.filter(
        Receita.nome.ilike('%{}%'.format(busca))).all()

    return serialize(receita)


@receitas.route('/<int:receita_id>')
def buscar_por_id(receita_id: int):
    receita: Receita = Receita.query.get(receita_id)

    if receita is None:
        abort(404)

    ignore_email = lambda prop: prop[0] != 'email'
    return receita.serialize(ignore=ignore_email), 200

