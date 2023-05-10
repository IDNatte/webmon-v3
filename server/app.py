from flask import Flask

import json

from controller import main
from controller.api import upload_api
from controller.api import error_api


def init_app(test_config=None):
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_file("./config/config.json", load=json.load)

    # API entrypoint
    app.register_blueprint(upload_api.upload_endpoint)

    # error handler
    app.register_blueprint(error_api.error_endpoint)

    # main entrypoint
    app.register_blueprint(main)

    app.config.get("UPLOAD_FOLDER")

    return app
