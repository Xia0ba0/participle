import datetime
import os
import math

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


def naive_bayes(classes, article, model):
    result = []
    sum_length = 0
    for _class in classes:
        sum_length += _class.length
    bag = article2bag(article, model)
    for _class in classes:
        result.append(cal_prob(sum_length, _class, bag))
    sort_result = sorted(result, key=lambda x: x[1], reverse=True)
    print(sort_result)
    return sort_result[0][0]


def article2bag(article, model):
    bag = {}
    for word in model:
        bag[word] = (article.tf.get(word, 0) * article.total_count)
    return bag


def cal_prob(sum_length, _class, bag):
    result = 0
    for word in bag:
        son = _class.term_in(word) + 1
        mother = _class.total_words + _class.length
        result += math.log(son / mother, 2)
    result += math.log(_class.length / sum_length, 2)
    return (_class.tag, result)
