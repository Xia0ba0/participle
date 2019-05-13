import math
import json
import os


class Class:
    def __init__(self, resolver, path, tag):
        self.tag = tag
        self.path = path
        self.articles = resolver.resolve_dir(path, tag=tag)
        self.length = len(self.articles)

    def term_in(self, term):
        count = 0
        for article in self.articles:
            if term in article.tf:
                count += 1
        return count

    def term_not_in(self, term, classes):
        count = 0
        for _class in classes:
            if _class.tag == self.tag:
                continue
            else:
                for article in _class.articles:
                    if term in article.tf:
                        count += 1

        return count

    @staticmethod
    def get_chi(classes):
        chi = {}
        class_count = len(classes)
        total_article_count = 0
        for _class in classes:
            total_article_count += _class.length

        print("Generating ------> " + ".\chi.json" + ".......")
        for _class in classes:
            chi[_class.tag] = {}
            for article in _class.articles:
                for term in article.tf:
                    df = Class.get_df(classes, term)
                    df_not = total_article_count - df + 1
                    term_in_class_count = _class.term_in(term)
                    no_term_in_class_count = _class.length - term_in_class_count
                    term_not_in_class_count = _class.term_not_in(term, classes)
                    no_term_not_in_class_count = total_article_count - _class.length - term_not_in_class_count

                    chi[_class.tag][term] = pow(
                        term_in_class_count * no_term_not_in_class_count - no_term_in_class_count * term_not_in_class_count,
                        2) / (df * df_not)

            chi_json = json.dumps(chi, sort_keys=True, indent=4, separators=(',', ': '))
            file = open('./chi.json', 'w')
            file.write(chi_json)
            file.close()

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
                    df_not = total_article_count - df + 1

                    for _class_cal in classes:
                        term_in_class_count = _class_cal.term_in(term) + 1
                        term_not_in_class_count = _class_cal.length - term_in_class_count + 2

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


class Classifier:
    def __init__(self, chi_dic=None, chi_json_file=r'.\idf.json'):
        if chi_dic is None:
            f = open(chi_json_file, 'r')
            chi_dic = json.load(f)
