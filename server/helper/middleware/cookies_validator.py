from flask import request
from functools import wraps

from helper.utils import auth_header_parser
from helper.error import auth_error
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
                raise auth_error.AuthError("TOKENInvalid", "Token key not match", 401)

        except KeyError:
            raise auth_error.AuthError(
                "TOKENError", "Authorization Header Missing", 401
            )

    return verify_auth_token
