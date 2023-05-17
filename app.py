from flask_migrate import Migrate
from flask import Flask

import json

from controller import main
from controller.api import upload_api
from controller.api import error_api

from helper.constant import DB
from model import User


def init_app(test_config=None):
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_file("./config/config.json", load=json.load)

    # database initializer
    DB.init_app(app)
    Migrate(app, db=DB).init_app(app, db=DB)

    # API entrypoint
    app.register_blueprint(upload_api.upload_endpoint)

    # error handler
    app.register_blueprint(error_api.error_endpoint)

    # main entrypoint
    app.register_blueprint(main)

    app.config.get("UPLOAD_FOLDER")

    return app
