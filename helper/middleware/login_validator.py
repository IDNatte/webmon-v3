from flask import redirect
from flask import session
from flask import url_for
from flask import flash
from flask import abort
from functools import wraps

from model import User


def login_required(function):
    @wraps(function)
    def verify_login(*args, **kwargs):
        if "wid" in session:
            user_data = User.query.get(session.get("wid"))
            return function(
                {"username": user_data.username, "token": user_data.token},
                *args,
                **kwargs
            )

        else:
            flash("Please login first", "error")
            return redirect(url_for("main.login"))

    return verify_login
