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
from helper.utils.utils_helper import file_renamer

from helper.constant.constant import DB
from model.report import ReportLog
from model.user import User

upload_endpoint = Blueprint("upload_api", __name__)

CORS(upload_endpoint)


@upload_endpoint.route("/upload", methods=["POST"])
@verify_token
def file_upload(account):
    print(account)
    try:
        fileup = request.files["file"]

        if fileup.filename == "":
            return jsonify({"failed": "no file provided"})

        if fileup and file_validator(fileup.filename):
            filename = secure_filename(file_renamer(fileup.filename))
            reporter_account_folder = os.path.isdir(
                os.path.join(
                    os.path.abspath(current_app.config["UPLOAD_FOLDER"]),
                    account.get("storage"),
                )
            )

            if reporter_account_folder:
                fileup.save(
                    os.path.join(
                        os.path.abspath(current_app.config["UPLOAD_FOLDER"]),
                        account.get("storage"),
                        filename,
                    )
                )

            else:
                os.mkdir(
                    os.path.join(
                        os.path.abspath(current_app.config["UPLOAD_FOLDER"]),
                        account.get("storage"),
                    )
                )

                fileup.save(
                    os.path.join(
                        os.path.abspath(current_app.config["UPLOAD_FOLDER"]),
                        account.get("storage"),
                        filename,
                    )
                )

            user = User.query.filter_by(token=account.get("token")).first()
            report_log = ReportLog(filename=filename, owner=user.id)
            DB.session.add(report_log)
            DB.session.commit()

            return jsonify({"saved": True, "time": datetime.datetime.now()})

        abort(401)

    except KeyError:
        abort(401)
