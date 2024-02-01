from helper.constant.constant import DB

from helper.database.database_helper import random_id_generator
from helper.database.database_helper import token_generator


class User(DB.Model):
    __tablename__ = "webmon_user"

    id = DB.Column(
        DB.String(200), primary_key=True, nullable=False, default=random_id_generator
    )
    username = DB.Column(DB.String(50), nullable=False)
    password = DB.Column(DB.String(200), nullable=False, unique=True)
    token = DB.Column(
        DB.String(200), nullable=False, unique=True, default=token_generator
    )
    storage_medium = DB.Column(
        DB.String(200), nullable=False, default=random_id_generator
    )

    report_log = DB.relationship("ReportLog", backref="user", lazy=True)
