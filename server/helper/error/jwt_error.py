class JWTError(Exception):
    """
    User Agent Exception error
    """

    def __init__(self, name, description, code):
        self.name = name
        self.description = description
        self.code = code
