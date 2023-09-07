from http import HTTPStatus as HTTP
from flask.helpers import flash, url_for
from flask.globals import g, session, current_app
from werkzeug.utils import redirect

from models.usuario.usuario import Usuario
from blueprints.utils import requer_autenticacao, requer_usuario_anonimo
from .blueprint import bp_conta


@bp_conta.route('/criar', methods=['POST'])
def criar():
    try:
        usuario: Usuario = Usuario.from_form(g.form)
        usuario.save(commit=True)
    except :
        return 404
    return redirect(url_for('.entrar'))


@bp_conta.route('/excluir', methods=['POST'])
@requer_autenticacao
def deletar():
    current_app.logger.debug('')
    usuario: Usuario = g.usuario
    usuario.delete(commit=True)

    flash("We're sorry to see you go :(")
    return redirect(url_for('.sair'))


@bp_conta.route('/autenticar', methods=['POST'])
@requer_usuario_anonimo()
def autenticar():
    form = g.form

    usuario = Usuario.query.filter_by(email=form.email.data).one_or_none()

    if usuario and usuario.more.is_active:
        if usuario.senha == form.senha.data:
            session['usuario_id'] = usuario.id
            return redirect(url_for('usuario'))

    flash("Email or Password doesn't match")
    return HTTP.NOT_FOUND


@bp_conta.route('/sair', methods=['GET', 'POST'])
def sair():
    """Rota para deslogar usuario"""
    session.clear()
    return redirect(url_for('main.index'))
