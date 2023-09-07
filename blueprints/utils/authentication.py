from blueprints.errorhandlers.exceptions import ApiUnauthorizedException, UnauthenticatedUserException
import http
import typing as t
from functools import wraps
from lib.helpers import is_user_authenticated
from flask.globals import g, current_app
from flask.helpers import flash, url_for
from sqlalchemy.orm import session
from werkzeug.utils import redirect


def authentication_required(view):
    """Decorator that restricts view access only to logged in users."""

    @wraps(view)
    def wrapper(*args, **kwargs):
        if g.usuario is None:
            raise UnauthenticatedUserException
        return view(*args, **kwargs)
    return wrapper


_DEFAULT_REDIRECT_TO = 'main.index'
def redirect_if_authenticated(to: t.Union[str, t.Callable]):
    """Decorator that redirects to another view if user is logged in."""

    def decorator(view):
        @wraps(view)
        def wrapper(*args, **kwargs):
            if is_user_authenticated():
                return redirect(url_for(kwargs.pop('r_to', None) or to))
            return view(*args, **kwargs)
        return wrapper

    if type(to) is not str:
        if callable(to):
            # decorator was used without parentheses
            return decorator(to, r_to=_DEFAULT_REDIRECT_TO)
        else:
            raise TypeError('Wrong argument type: %s' % type(to))

    return decorator
