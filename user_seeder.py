from app import init_app
from model import User
from helper.constant import DB as db
from helper.security import password_module


def seed_user():
    users = [
        {"username": "admin", "password": password_module.create_password("admin")}
    ]

    with init_app().app_context():
        for user_data in users:
            user = User(**user_data)
            db.session.add(user)

        db.session.commit()


if __name__ == "__main__":
    seed_user()
