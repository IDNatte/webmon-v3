from werkzeug.utils import secure_filename

from flask import current_app
from flask import Blueprint
from flask import jsonify
from flask import request
from flask import abort

import datetime
import os

from flask_cors import CORS

from helper.middleware.token_validator import verify_token
from helper.validator.file_validator import file_validator
from helper.utils import file_renamer


upload_endpoint = Blueprint("upload_api", __name__)

CORS(upload_endpoint)


@upload_endpoint.route("/upload", methods=["POST"])
@verify_token
def file_upload():
    try:
        fileup = request.files["file"]

        if fileup.filename == "":
            return jsonify({"failed": "no file provided"})

        if fileup and file_validator(fileup.filename):
            filename = secure_filename(file_renamer(fileup.filename))

            fileup.save(
                os.path.join(
                    os.path.abspath(current_app.config["UPLOAD_FOLDER"]), filename
                )
            )

            return jsonify({"saved": True, "time": datetime.datetime.now()})

        abort(401)

    except KeyError:
        abort(401)
