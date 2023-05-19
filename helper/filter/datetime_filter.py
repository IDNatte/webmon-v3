import datetime


def datetime_costume_filter(tstamp):
    return datetime.datetime.strptime(tstamp, "%Y-%m-%d %H:%M:%S.%f").strftime(
        "%A, %B %d %Y at %H:%M:%S"
    )


def datetime_server_filter(tstamp):
    return datetime.datetime.strptime(tstamp, "%Y%m%d%H%M%S%z").strftime(
        "%A, %B %d %Y at %H:%M:%S"
    )
