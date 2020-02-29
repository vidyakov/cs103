from collections import Counter, defaultdict
from math import log


class NaiveBayesClassifier:
    def __init__(self, alpha=0.05):
        self.alpha = alpha
        self.classes = {}
        self.words = {}

    def fit(self, x, y):
        """ Fit Naive Bayes classifier according to X, y. """
        table = defaultdict(dict)
        p = {key: value / len(y) for key, value in Counter(y).items()}

        for title, mark in zip(x, y):
            words = Counter(title.split())
            for word, count in words.items():
                if mark in table[word]:
                    table[word][mark] += count
                else:
                    table[word][mark] = count

        d = len(table)
        for word, dic in table.items():
            for mark, value in p.items():
                table[word][f'{word}|{mark}'] = (dic.get(mark) if dic.get(mark) is not None else 0 + self.alpha) / \
                    (sum([table[word].get(i) if table[word].get(i) is not None else 0 for i in p]) + self.alpha * d)

        self.classes = p
        self.words = table

    def predict(self, x):
        """ Perform classification on an array of test vectors X. """
        predictions = []
        for title in x:
            words = Counter(title.split())
            marks = {}
            for mark, value in self.classes.items():
                elements = [log(value)]
                for word, total in words.items():
                    elements.append(log(self.words.get(word)[f'{word}|{mark}']) * total
                                    if self.words.get(word) is not None else 0)
                marks[mark] = sum(elements)

            for key, value in marks.items():
                if value == max(marks.values()):
                    predictions.append(key)

        return predictions

    def score(self, x_test, y_test):
        """ Returns the mean accuracy on the given test data and labels. """
        t = 0
        for x, y in zip(self.predict(x_test), y_test):
            if x == y:
                t += 1
        return t / len(y_test)

    def export(self):
        """ Export the trained model to JSON """
        pass



import csv
import string

with open("data/SMSSpamCollection") as f:
    data = list(csv.reader(f, delimiter="\t"))

def clean(s):
    translator = str.maketrans("", "", string.punctuation)
    return s.translate(translator)
X, y = [], []
for target, msg in data:
        X.append(msg)
        y.append(target)

X = [clean(x).lower() for x in X]
X_train, y_train, X_test, y_test = X[:3900], y[:3900], X[3900:], y[3900:]

model = NaiveBayesClassifier(0.05)
model.fit(X_train, y_train)
model.predict(X_test)
print(model.score(X_test, y_test))
