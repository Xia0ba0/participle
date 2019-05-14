import math
import json
import os


class Class:
    def __init__(self, resolver, path, tag):
        self.tag = tag
        self.path = path
        self.articles = resolver.resolve_dir(path, tag=tag)
        self.length = len(self.articles)

        self.total_words = 0
        for article in self.articles:
            self.total_words += article.total_count

    def get_term_in(self, term):
        times = 0
        for article in self.articles:
            if term in article.tf:
                times += article.tf[term]*article.total_count
        return times

    def get_term_info(self, term, classes):
        have_and_in = 0
        have_and_not_in = 0
        no_and_in = 0
        no_and_not_in = 0

        for _class in classes:
            if self.tag == _class.tag:
                for article in _class.articles:
                    if term in article.tf:
                        have_and_in += 1
                    else:
                        no_and_in += 1
            else:
                for article in _class.articles:
                    if term in article.tf:
                        have_and_not_in += 1
                    else:
                        no_and_not_in += 1

        return {"have_and_in": have_and_in,
                "have_and_not_in": have_and_not_in,
                "no_and_in": no_and_in,
                "no_and_not_in": no_and_not_in}

    @staticmethod
    def get_classes(root_dir, resolver):
        tags = os.listdir(root_dir)
        classes = []

        for tag in tags:
            classes.append(Class(resolver, os.path.join(root_dir, tag), tag))

        return classes

    @staticmethod
    def get_chi(classes):
        chi = {}
        total_article_count = 0
        for _class in classes:
            total_article_count += _class.length

        print("Generating ------> " + ".\chi.json" + ".......")
        for _class in classes:
            chi[_class.tag] = {}
            for article in _class.articles:
                for term in article.tf:
                    if term in chi:
                        continue
                    else:
                        info = _class.get_term_info(term, classes)
                        df = info["have_and_in"] + info["have_and_not_in"]
                        df_not = info["no_and_in"] + info["no_and_not_in"] + 1

                        chi[_class.tag][term] = pow(
                            info["have_and_in"] * info["no_and_not_in"] - info["no_and_in"] * info["have_and_not_in"],
                            2) / (df * df_not)

            chi_json = json.dumps(chi, sort_keys=True, indent=4, separators=(',', ': '))
            file = open('./chi.json', 'w')
            file.write(chi_json)
            file.close()

    @staticmethod
    def get_feature():
        feature = []
        f = open('./chi.json', 'r')
        chi_dic = json.load(f)
        for _class, dic in chi_dic.items():
            sort_tup = sorted(dic.items(), key=lambda x: x[1], reverse=True)[0:100]
            count = 0
            for word, value in sort_tup:
                if word in feature:
                    continue
                feature.append(word)
                count += 1

                if count == 4:
                    break
        print(feature)
        return feature

    @staticmethod
    def naive_bayes_train(classes, feature):
        model = {}
        print("Generating ------> " + ".\model.json" + ".......")
        for _class in classes:
            model[_class.tag] = {}

            for word in feature:
                model[_class.tag][word] = 1 + _class.get_term_in(word)

            total_count = sum(model[_class.tag].values())
            len_of_feature = len(feature)
            for word in feature:
                model[_class.tag][word] = model[_class.tag][word] / (total_count + len_of_feature)

        model_json = json.dumps(model, sort_keys=True, indent=4, separators=(',', ': '))
        file = open('./model.json', 'w')
        file.write(model_json)
        file.close()