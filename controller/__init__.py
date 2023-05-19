from flask import render_template
from flask import current_app
from flask import Blueprint
from flask import redirect
from flask import request
from flask import session
from flask import url_for
import msgpack
import os


from helper.middleware.login_validator import login_required
from helper.security.password_module import check_passwd

from helper.filter.datetime_filter import datetime_costume_filter
from helper.filter.filename_readable import log_filename_readable
from helper.filter.bites_readable import format_bytes

from model import ReportLog
from model import User

main = Blueprint("main", __name__)


@main.app_template_filter("datetime_convert")
def datetime_converter(s):
    return datetime_costume_filter(s)


@main.app_template_filter("readable_bytes")
def bytes_humanizer(s):
    return format_bytes(s)


@main.app_template_filter("logname_readable")
def logname_readable(s):
    return log_filename_readable(s)


@main.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        account_checker = User.query.filter_by(username=username).first()

        if account_checker and check_passwd(account_checker.password, password) == True:
            session["wid"] = str(account_checker.id)
            return redirect(url_for("main.index"))

        else:
            error = "Invalid username or password"
            return render_template("template/login/index.html", error=error)
    else:
        return render_template("template/login/index.html")


@main.route("/")
@login_required
def index(account):
    users = User.query.filter_by(token=account.get("token"))
    log_content_lists = (
        ReportLog.query.join(User)
        .filter(User.token == account.get("token"))
        .order_by(ReportLog.uploaded.desc())
        .all()
    )

    try:
        with open(
            os.path.join(
                current_app.config.get("UPLOAD_FOLDER"),
                account.get("storage"),
                log_content_lists[0].filename,
            ),
            "rb",
        ) as binary:
            raw_content = binary.read()

            content = msgpack.unpackb(raw_content)
        return render_template(
            "template/admin/index.html",
            history=log_content_lists,
            account=account,
            content=content,
            user=users,
        )

    except (
        IndexError,
        FileNotFoundError,
        msgpack.exceptions.ExtraData,
        msgpack.exceptions.FormatError,
    ):
        return render_template("template/admin/index.html", account=account, user=users)


@main.route("/log_history/<report_id>")
@login_required
def read_history(account, report_id):
    users = User.query.all()
    report = ReportLog.query.get(report_id)

    try:
        with open(
            os.path.join(
                current_app.config.get("UPLOAD_FOLDER"),
                account.get("storage"),
                report.filename,
            ),
            "rb",
        ) as rep_hist_bin:
            raw_content = rep_hist_bin.read()

            content = msgpack.unpackb(raw_content)
            return render_template(
                "template/log_history/index.html",
                history_at=report.uploaded,
                account=account,
                content=content,
            )

    except (
        IndexError,
        FileNotFoundError,
        msgpack.exceptions.ExtraData,
        msgpack.exceptions.FormatError,
    ):
        return render_template(
            "template/log_history/index.html", account=account, user=users
        )


@main.route("/logout")
@login_required
def logout(_):
    session.pop("wid", None)
    return redirect(url_for("main.login"))
