from flask_migrate import Migrate
from flask import Flask

from getpass import getpass

import click
import json

from controller import main
from controller.api import upload_api
from controller.api import error_api

from helper.security.password_module import create_password

from helper.constant import DB
from model import User


def init_app(test_config=None):
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_file("./config/config.json", load=json.load)

    # database initializer
    DB.init_app(app)
    Migrate(app, db=DB).init_app(app, db=DB)

    # seeder
    @app.cli.command("create-user")
    @click.argument("name")
    def create_user(name):
        password = getpass("Enter password : ")
        confirm_pass = getpass("Re-Enter your password : ")

        if confirm_pass == password:
            is_available = User.query.filter_by(username=name).first()

            if not is_available:
                add_user = User(username=name, password=create_password(password))
                DB.session.add(add_user)
                DB.session.commit()
                print(f"[*] User {name} created !")

            else:
                print("[!] User already registered")

        else:
            print("\n[!] Password did not match\n")

    # API entrypoint
    app.register_blueprint(upload_api.upload_endpoint)

    # error handler
    app.register_blueprint(error_api.error_endpoint)

    # main entrypoint
    app.register_blueprint(main)

    app.config.get("UPLOAD_FOLDER")

    return app