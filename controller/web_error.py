from flask import render_template
from flask import Blueprint


web_error = Blueprint("web_error", __name__)


@web_error.app_errorhandler(404)
def not_found_handler(error):
    return render_template("template/error/index.html")
