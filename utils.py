import datetime
import os
import json

import jieba


def exe_time(func):
    def new_func(*args, **kwargs):
        start_time = datetime.datetime.now()
        result = func(*args, **kwargs)
        end_time = datetime.datetime.now()

        return result, (end_time - start_time).total_seconds()

    return new_func


def get_size(filename):
    return os.path.getsize(filename)


def get_real_cut(filename):
    file = open(filename)
    seg_list = jieba.cut(file.read(), cut_all=True)
    return list(seg_list)