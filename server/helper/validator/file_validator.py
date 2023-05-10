from flask import current_app


def file_validator(filename):
    return "." in filename and filename.rsplit(".", 1)[
        1
    ].lower() in current_app.config.get("ALLOWED_EXTENSIONS")
