from http import HTTPStatus as HTTP
from models.usuario.usuario import Usuario
from typing import List
from flask import abort, request
from flask.globals import current_app, g
from flask.helpers import make_response, url_for
from werkzeug.utils import redirect
from werkzeug.wrappers.response import Response

from blueprints.api.lib import api
from blueprints.utils import requer_autenticacao
from forms.receitas import ReceitaForm
from models.receitas import Receita
from models.serialization import serialize
from ..blueprint import bp_receitas


@bp_receitas.route('/')
def listar():
    receita: List[Receita] = Receita.query.all()
    return serialize(receita)


@bp_receitas.route('/buscar', defaults={'busca': ''})
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


@bp_receitas.route('/', methods=['POST'])
@requer_autenticacao
@api.query
def criar():
    receita = Receita()
    form = ReceitaForm.from_json(request.json)
    form.populate_obj(receita)
    receita.criador = g.usuario

    # api.validate(form.validate(), form.errors, )
    api.validate(receita.save(commit=True), 'Erro ao salvar',
                 HTTP.INTERNAL_SERVER_ERROR)

    return receita.serialize()


@bp_receitas.route('/', methods=['PUT'], defaults={'receita_id': ''})
@bp_receitas.route('/<int:receita_id>', methods=['POST'])
@requer_autenticacao
@api.query
def editar(receita_id: int):
    if not receita_id:
        receita_id = request.json.get('id')
    usuario_id = request.json.get('criador', {}).get('id')

    api.validate(receita_id and usuario_id, http_error=HTTP.BAD_REQUEST)

    del request.json['criador']

    receita: Receita = Receita.query.filter_by(id=receita_id).one_or_none()

    api.validate(receita is not None, 'Receita não existe.')

    form: ReceitaForm = ReceitaForm.from_json(request.json)
    form.populate_obj(receita)

    # api.validate(receita.criador is g.usuario,
    #     'Você não tem permissão para excluir esta receita!', HTTP.UNAUTHORIZED)

    api.validate(form.validate(), form.errors)
    api.validate(receita.save(commit=True), 'Não foi possivel salvar. '
                 'Erro desconhecido', HTTP.INTERNAL_SERVER_ERROR)

    return receita.serialize()


@bp_receitas.route('/<int:receita_id>', methods=['DELETE'])
@requer_autenticacao
@api.query
def deletar(receita_id: int):
    receita: Receita = Receita.query.filter_by(id=receita_id).one_or_none()

    api.validate(receita is not None,'Receita não existe.', HTTP.BAD_REQUEST)
    # api.validate(receita.criador is g.usuario,
    #     'Você não tem permissão para excluir esta receita!', HTTP.UNAUTHORIZED)
    api.validate(receita.delete(commit=True), 'Não foi possível excluir esta'
                ' receita. Entre em contato conosco para mais detalhes',
                HTTP.INTERNAL_SERVER_ERROR)

    return '', HTTP.OK
