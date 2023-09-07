from flask.globals import g, session, current_app

from models.usuario.usuario import Usuario
from .blueprint import bp_conta


@bp_conta.before_app_request
def anexa_usuario_autenticado():
    g.usuario = None

    if usuario_id := session.get('usuario_id') is not None:
        usuario: Usuario = Usuario.query.filter(id=usuario_id).one_or_none()
        if usuario is not None and not usuario.isdeleted():
            g.usuario = usuario
        else:
            del session['usuario_id']
