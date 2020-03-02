from db import News, session
from pprint import pprint
import string
from bayes import NaiveBayesClassifier

def clean(s):
    translator = str.maketrans("", "", string.punctuation)
    return s.translate(translator)

s = session()
titles = [clean(news.title).lower() for news in s.query(News).filter(News.label != None).all()]
marks = [news.label for news in s.query(News).filter(News.label != None).all()]

print(len(titles), len(marks))
pprint(titles[:4])

seventy_percent = round(len(titles) * 0.70)


x_train, y_train, x_test, y_test = titles[:seventy_percent], marks[:seventy_percent], titles[seventy_percent:], marks[seventy_percent:]
model = NaiveBayesClassifier()
model.fit(x_train, y_train)
print(model.score(x_test, y_test))
model.export_model('news_model.json')
