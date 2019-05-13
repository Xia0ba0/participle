import math
import json
import os


class Class:
    def __init__(self, resolver, path, tag):
        self.tag = tag
        self.path = path
        self.articles = resolver.resolve_dir(path, tag)
        self.length = len(self.articles)

    def term_in(self, term):
        count = 0
        for article in self.articles:
            if term in article.tf:
                count += 1
        return count

    @staticmethod
    def get_classes(root_dir, resolver):
        tags = os.listdir(root_dir)
        classes = []

        for tag in tags:
            classes.append(Class(resolver, os.path.join(root_dir, tag), tag))

        return classes

    @staticmethod
    def get_ig(classes):
        ig = {}
        class_count = len(classes)
        total_article_count = 0
        for _class in classes:
            total_article_count += _class.length

        hc = 0 - class_count * math.log(1 / class_count, 2)

        for _class in classes:
            for article in _class.articles:
                for term in article.tf:
                    if term in ig:
                        continue

                    ig[term] = hc
                    df = Class.get_df(classes, term)
                    df_not = total_article_count - df

                    for _class_cal in classes:
                        term_in_class_count = _class_cal.term_in(term)
                        term_not_in_class_count = _class_cal.length - term_in_class_count

                        ig[term] += (df / total_article_count) * (term_in_class_count / df) * math.log(
                            term_in_class_count / df, 2)
                        ig[term] += (df_not / total_article_count) * (term_not_in_class_count / df_not) * math.log(
                            term_not_in_class_count / df_not, 2)

            ig_json = json.dumps(ig, sort_keys=True, indent=4, separators=(',', ': '))
            file = open('./ig.json', 'w')
            file.write(ig_json)
            file.close()

    @staticmethod
    def get_df(classes, term):
        count = 0
        for _class in classes:
            for article in _class.articles:
                if term in article.tf:
                    count += 1
        return count
