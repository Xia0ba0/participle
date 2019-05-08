import datetime
import os


def exe_time(func):
    def new_func(*args, **kwargs):
        start_time = datetime.datetime.now()
        func(*args, **kwargs)
        end_time = datetime.datetime.now()

        return (end_time - start_time).total_seconds()

    return new_func


def get_size(filename):
    return os.path.getsize(filename)
