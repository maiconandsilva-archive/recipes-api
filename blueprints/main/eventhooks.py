from .blueprint import bp_main


@bp_main.before_app_request
def anexar_formulario():
    pass
