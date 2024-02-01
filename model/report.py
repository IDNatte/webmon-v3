from helper.constant import DB

from helper.database import random_id_generator
from helper.database import token_generator

from sqlalchemy import func



class ReportLog(DB.Model):
    __tablename__ = "webmon_reporter"

    id = DB.Column(
        DB.String(200), primary_key=True, nullable=False, default=random_id_generator
    )
    filename = DB.Column(DB.String(200), nullable=False)
    uploaded = DB.Column(DB.DateTime, default=func.now())
    owner = DB.Column(DB.String(200), DB.ForeignKey("webmon_user.id"), nullable=False)