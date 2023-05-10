from flask import render_template
from flask import Blueprint
from flask import jsonify

from flask_cors import CORS

main = Blueprint("main", __name__)

CORS(main)


@main.route("/")
def index():
    return render_template("index.html")
