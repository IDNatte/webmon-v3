from flask import request
from functools import wraps

from helper.utils import auth_header_parser
from helper.error.auth_error import AuthApiError
from model import User


def verify_token(function):
    """
    verify token
    """

    @wraps(function)
    def verify_auth_token(*args, **kwargs):
        try:
            token_header = request.headers["Authorization"]
            token = auth_header_parser(token_header)

            validator = User.query.filter_by(token=token).first()

            if validator:
                return function(*args, **kwargs)

            else:
                raise AuthApiError("TOKENInvalid", "Token key not match", 401)

        except KeyError:
            raise AuthApiError("TOKENError", "Authorization Header Missing", 401)

    return verify_auth_token
