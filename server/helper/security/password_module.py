from passlib.hash import pbkdf2_sha256


def create_password(password):
    return pbkdf2_sha256.hash(password)


def check_passwd(comparator, password):
    return pbkdf2_sha256.verify(password, comparator)
