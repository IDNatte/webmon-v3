import datetime


def datetime_costume_filter(tstamp):
    return datetime.datetime.strptime(tstamp, "%Y-%m-%d %H:%M:%S.%f").strftime(
        "%A, %B %d %Y at %H:%M:%S"
    )
