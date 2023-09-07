import functools
import http
from flask.globals import g

from models.usuario.usuario import Usuario
from ..errorhandlers.exceptions import ApiControledServerException, ApiUnauthorizedException, ApiValidationException


def _api_wrapper(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        return f(*args, **kwargs)
    return wrapper


class _API:
    def __call__(self, f, *args, **kwargs):
        return _api_wrapper(f)

    def query(self, f):
        return _api_wrapper(f)

    def validate(self, valid, message=None, http_error=None):
        if not valid:
            raise ApiValidationException(message, http_error)

    def verify(self, valid, message=None, http_error=None):
        self._assert(valid, ApiControledServerException(message, http_error))

    def isauthorized(self, usuario, message=None, http_error=None):
        self._assert(usuario is g.usuario,
                     ApiUnauthorizedException(message, http_error))

    def _assert(self, assertion, exception):
        if not assertion:
            raise exception


api = _API()

