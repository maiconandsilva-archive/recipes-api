"""Application error handlers."""

import http
from flask import Blueprint, jsonify
from werkzeug.exceptions import InternalServerError
from .blueprint import bp_errors

from .exceptions import ApiException, ApiValidationException


@bp_errors.app_errorhandler(InternalServerError)
def handle_unexpected_error(error: InternalServerError):
    return {
        'success': False,
        'error': {
            'type': error.__class__.__name__,
            'description': error.description
        }
    }, error.code


@bp_errors.app_errorhandler(ApiValidationException)
def handle_error(error: ApiException):
    return error.response()
