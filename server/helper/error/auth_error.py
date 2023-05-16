class AuthApiError(Exception):
    """
    Authentication error

    Error related to Authentication.
    """

    def __init__(self, name, description, code):
        self.name = name
        self.code = code
        self.description = description
