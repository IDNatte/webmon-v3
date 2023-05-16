from flask import render_template
from flask import current_app
from flask import Blueprint
from flask import redirect
from flask import jsonify
from flask import request
import msgpack
import os

from flask_cors import CORS

from helper.filter.datetime_filter import datetime_costume_filter
from helper.security.password_module import create_password
from helper.security.password_module import check_passwd
from helper.filter.bites_readable import format_bytes

from model import User

main = Blueprint("main", __name__)

CORS(main)


@main.app_template_filter("datetime_convert")
def datetime_converter(s):
    return datetime_costume_filter(s)


@main.app_template_filter("readable_bytes")
def bytes_humanizer(s):
    return format_bytes(s)


@main.route("/test")
def testing():
    testing = sorted(
        os.listdir(os.path.join(current_app.config.get("UPLOAD_FOLDER"))), reverse=True
    )
    try:
        with open(
            os.path.join(current_app.config.get("UPLOAD_FOLDER"), testing[0]), "rb"
        ) as test:
            raw_content = test.read()

            content = msgpack.unpackb(raw_content)
        return jsonify(content)

    except IndexError:
        return jsonify({"content": None})


@main.route("/error_test")
def error_test():
    return render_template("template/error/index.html")


@main.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        account_checker = User.query.filter_by(username=username).first()

        if account_checker and check_passwd(account_checker.password, password) == True:
            print("coba")
            return render_template("template/login/index.html")

        else:
            error = "Invalid username or password"
            return render_template("template/login/index.html", error=error)
    else:
        return render_template("template/login/index.html")


@main.route("/")
def index():
    users = User.query.all()
    log_data = sorted(
        os.listdir(os.path.join(current_app.config.get("UPLOAD_FOLDER"))), reverse=True
    )
    try:
        with open(
            os.path.join(current_app.config.get("UPLOAD_FOLDER"), log_data[0]), "rb"
        ) as test:
            raw_content = test.read()

            content = msgpack.unpackb(raw_content)
        return render_template("template/admin/index.html", content=content, user=users)

    except IndexError:
        return render_template("template/admin/index.html", user=users)
