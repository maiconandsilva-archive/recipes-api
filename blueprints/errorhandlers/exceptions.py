from werkzeug.exceptions import HTTPException

import http
from flask import Blueprint, jsonify


class UnauthenticatedUserException(HTTPException):
    pass


class ApiException(HTTPException):
    code = http.HTTPStatus.INTERNAL_SERVER_ERROR

    def __init__(self, message='', http_error=None, /, *args, **kwargs):
        self.message = message
        if http_error:
            self.code = http_error
        super().__init__(*args, **kwargs)

    @property
    def response(self):
        return {
            'success': False,
            'error': {
                'type': self.__class__.__name__,
                'message': self.message,
            }
        }, self.code


class NotFoundException(HTTPException):
    code = http.HTTPStatus.NOT_FOUND


class ApiControledServerException(ApiException):
    """"""


class ApiClientException(ApiException):
    code = http.HTTPStatus.BAD_REQUEST


class ApiUnauthorizedException(ApiClientException):
    code = http.HTTPStatus.UNAUTHORIZED


class ApiValidationException(ApiClientException):
    """Raised when a validator fails to validate its input."""

    def __init__(self, message, http_error, /, *args, **kwargs):
        if message is not None:
            message = 'Não foi possivel concluir a operação.'
        super().__init__(message, http_error, *args, **kwargs)

    @property
    def response(self):
        _response = super().response
        # if self.form.errors:
        #     _response['error']['form'] = self.form.errors
        return _response
