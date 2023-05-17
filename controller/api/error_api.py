from flask import Blueprint
from flask import jsonify

from flask_cors import CORS

from helper.error.auth_error import AuthApiError

error_endpoint = Blueprint("error_api", __name__)

CORS(error_endpoint)


@error_endpoint.app_errorhandler(AuthApiError)
def app_error_handler(error):
    return (
        jsonify(
            {"status": error.name, "code": error.code, "detail": error.description}
        ),
        error.code,
    )
