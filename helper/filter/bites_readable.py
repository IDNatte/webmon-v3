import math


def format_bytes(size):
    power = 0 if size <= 0 else math.floor(math.log(size, 1024))
    return (
        f"{round(size / 1024 ** power, 2)} {['B', 'KB', 'MB', 'GB', 'TB'][int(power)]}"
    )
