from helper.error.auth_error import AuthApiError
import datetime


def file_renamer(filename):
    current_date = datetime.datetime.now()
    insert_timestamp = current_date.strftime("%Y%m%d_%H:%M:%SZ")
    file = filename.split(".")

    return f"{file[0]}_{insert_timestamp}.{file[1]}"


def auth_header_parser(headers):
    """
    Authorization header parser
    """
    parser = headers.split(" ")

    if parser[0] == "Bearer":
        if len(parser) == 2:
            return parser[1]
        else:
            raise AuthApiError("TOKENError", "Missing token", 401)
    else:
        raise AuthApiError("TOKENError", "Broken Authorization header", 401)


def filename_reverse(string):
    # print(list(string)[:8])
    # print(list(string)[8:])

    return {"testing": True}
