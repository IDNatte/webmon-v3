"""
Model Helper function
"""
import random
import string
import secrets


def random_id_generator():
    return "".join(
        (
            random.choice(string.ascii_letters + string.digits + string.punctuation)
            for x in range(50)
        )
    )


def token_generator():
    token = f"wmt-{secrets.token_urlsafe(32)}"
    return token
