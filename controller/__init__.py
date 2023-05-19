from flask import render_template
from flask import current_app
from flask import Blueprint
from flask import redirect
from flask import jsonify
from flask import request
from flask import session
from flask import url_for
import msgpack
import os

import datetime

from flask_cors import CORS

from helper.middleware.login_validator import login_required
from helper.security.password_module import check_passwd

from helper.filter.datetime_filter import datetime_costume_filter
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


# @main.route("/test")
# @login_required
# def testing(account):
#     try:
#         testing = sorted(
#             os.listdir(
#                 os.path.join(
#                     current_app.config.get("UPLOAD_FOLDER"), account.get("token")
#                 )
#             ),
#             reverse=True,
#         )

#         with open(
#             os.path.join(
#                 current_app.config.get("UPLOAD_FOLDER"),
#                 account.get("token"),
#                 testing[0],
#             ),
#             "rb",
#         ) as test:
#             raw_content = test.read()

#             content = msgpack.unpackb(raw_content)
#         return jsonify(content)

#     except IndexError:
#         return jsonify({"content": None})


# @main.route("/error_test")
# def error_test():
#     return render_template("template/error/index.html")


@main.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        account_checker = User.query.filter_by(username=username).first()

        if account_checker and check_passwd(account_checker.password, password) == True:
            session["wid"] = str(account_checker.id)
            return redirect("/")

        else:
            error = "Invalid username or password"
            return render_template("template/login/index.html", error=error)
    else:
        return render_template("template/login/index.html")


@main.route("/")
@login_required
def index(account):
    users = User.query.all()

    try:
        log_data = sorted(
            os.listdir(
                os.path.join(
                    current_app.config.get("UPLOAD_FOLDER"), account.get("token")
                )
            ),
            reverse=True,
        )

        # To-Do:
        # add log history
        testing = [ts.split("_") for ts in log_data]
        test2 = f"{testing[0][3]}{testing[0][4].split('.')[0]}"
        coba = datetime.datetime.strptime(test2, "%Y%m%d%H%M%S%z")
        print(coba.second)

        with open(
            os.path.join(
                current_app.config.get("UPLOAD_FOLDER"),
                account.get("token"),
                log_data[0],
            ),
            "rb",
        ) as test:
            raw_content = test.read()

            content = msgpack.unpackb(raw_content)
        return render_template(
            "template/admin/index.html", account=account, content=content, user=users
        )

    except (
        IndexError,
        FileNotFoundError,
        msgpack.exceptions.ExtraData,
        msgpack.exceptions.FormatError,
    ):
        return render_template("template/admin/index.html", account=account, user=users)


@main.route("/logout")
@login_required
def logout(_):
    session.pop("wid", None)
    return redirect(url_for("main.login"))
