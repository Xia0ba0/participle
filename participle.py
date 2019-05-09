#!/usr/bin/python
# -*- coding: UTF-8 -*-
from collections import Counter
import os
import math
import json
import re
import numpy

class Article:
    def __init__(self, filename, words):
        self.w = {}
        self.file_name = filename

        self.words = words
        self.total_count = len(words)

        self.tf = dict(Counter(words))
        for word in self.tf:
            self.tf[word] = self.tf[word] / self.total_count

    def get_w(self, idf_dic=None, idf_json_file=r'.\idf.json'):
        if idf_dic is None:
            f = open(idf_json_file, 'r')
            idf_dic = json.load(f)

        for word, tf_value in self.tf.items():
            self.w[word] = tf_value * idf_dic.get(word, 100)

    def get_top_10(self):
        return sorted(self.w.items(), key=lambda x: x[1], reverse=True)[0:10]

    @staticmethod
    def get_idf_json_file(articles):
        print("Generating ------> " + ".\idf.json" + ".......")
        n = len(articles)
        idf = {}

        for sample in articles:
            for word in sample.tf:
                if word in idf:
                    continue
                else:
                    df = 0
                    for article in articles:
                        if word in article.tf:
                            df = df + 1
                    idf[word] = math.log(n / df)

        idf_json = json.dumps(idf, sort_keys=True, indent=4, separators=(',', ': '))

        file = open('./idf.json', 'w')
        file.write(idf_json)
        file.close()

    @staticmethod
    def get_similarity(article1, article2):
        merge_words = {**article1.tf, **article2.tf}
        v1 = []
        v2 = []
        for word in list(merge_words):
            v1.append(article1.tf.get(word, 0))
            v2.append(article2.tf.get(word, 0))

        v1 = numpy.array(v1)
        v2 = numpy.array(v2)

        son = (v1 * v2).sum()
        monther = math.sqrt(numpy.square(v1).sum()) * math.sqrt(numpy.square(v2).sum())
        return son / monther


class Participle:
    words_set = set()
    max_length = 0
    articles_list = []

    def __init__(self, dic_file):
        with open(dic_file, 'r', encoding="gb18030", errors="ignore") as dic:
            while True:
                line = dic.readline().strip()
                length = len(line)

                if length == 0:
                    break
                elif length > self.max_length:
                    self.max_length = length

                self.words_set.add(line)

    def resolve_file(self, srcfile, article_object=True):
        result = []
        index = 0

        with open(srcfile, 'r', encoding="gb18030", errors="ignore") as src:
            text = re.sub(r'[^0-9A-Za-z\u4E00-\u9FFF]+', '', src.read())
            text_length = len(text)

        while index < text_length:
            for i in range(self.max_length, 0, -1):
                word = text[index:index + i]

                if word in self.words_set:
                    result.append(word)
                    index += i
                    break
                if i == 1:
                    result.append(word)
                    index += 1
                    break
        if article_object:
            return Article(srcfile, result)
        else:
            return result

    def resolve_dir(self, dir_name):
        self.articles_list = []
        for root, dirs, files in os.walk(dir_name, topdown=False):
            for file in files:
                full_path = os.path.join(root, file)
                print("Resolving  ------> " + full_path + ".......")
                self.articles_list.append(self.resolve_file(full_path))
