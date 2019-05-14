import json


class Classifier:
    def __init__(self):
        f = open('.\model.json', 'r')
        self.model = json.load(f)
        f.close()

        self.tags = list(self.model.keys())
        self.feature = self.model[self.tags[0]].keys()

    def classify(self, article):
        result = {}
        bag_of_word = article.article2bag(self.feature)

        for tag in self.tags:
            result[tag] = 1
            for word, value in bag_of_word.items():
                result[tag] = result[tag] * pow(self.model[tag][word], value)

        result = sorted(result.items(), key=lambda x: x[1], reverse=True)
        return result[0][0]
