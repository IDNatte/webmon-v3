from flask import request
from functools import wraps

from helper.utils import auth_header_parser
from helper.error import auth_error


def verify_jwt(function):
    """
    verify jwt token
    """

    @wraps(function)
    def verify_jwt_token(*args, **kwargs):
        try:
            token_header = request.headers["Authorization"]
            token = auth_header_parser(token_header)

            if token == "dev":
                return function(*args, **kwargs)

            else:
                raise auth_error.AuthError("JWTInvalid", "JWT key not match", 401)

        except KeyError:
            raise auth_error.AuthError("JWTError", "Authorization Header Missing", 401)

    return verify_jwt_token
