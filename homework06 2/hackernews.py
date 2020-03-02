from bottle import (
    route, run, template, request, redirect
)
from scraputils import get_news
from db import News, session
from bayes import NaiveBayesClassifier
import string
from collections import deque


@route('/')
@route("/news")
def news_list():
    s = session()
    rows = s.query(News).filter(News.label == None).all()
    return template('news_template', rows=rows)


@route("/add_label/")
def add_label():
    s = session()
    best_row = s.query(News).filter(News.id == request.params['id']).one()
    best_row.label = request.params['label']
    s.add(best_row)
    s.commit()
    redirect("/news")


@route("/update")
def update_news(pages=1):
    s = session()
    total = 0

    for new in get_news(n_pages=pages):
        if (s.query(News).filter(News.title == new['title']).one_or_none() is None) \
                and (s.query(News).filter(News.author == new['authors']).one_or_none() is None):
            new = News(
                        title=new['title'],
                        author=new['authors'],
                        url=new['link'],
                        comments=new['comments'],
                        points=new['points']
                    )
            s.add(new)
            total += 1

    if total == 0:
        update_news(pages+1)
    else:
        s.commit()
        redirect("/news")


def clean(s):
    translator = str.maketrans("", "", string.punctuation)
    return s.translate(translator)


@route("/classify")
def classify_news():
    s = session()
    rows = s.query(News).filter(News.label == None).all()

    model = NaiveBayesClassifier()
    model.import_model('news_model.json')
    predictions = model.predict([row.title for row in rows])

    d = deque()
    for new, pred in zip(rows, predictions):
        if pred == 'good':
            d.appendleft(new)
        elif pred == 'never':
            d.append(new)

    return template('classify', rows=d)


if __name__ == "__main__":
    run(host="localhost", port=1113)
