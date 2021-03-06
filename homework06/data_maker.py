import db
import scraputils as su
import random


s = db.session()
try:
    for dic in su.get_news(n_pages=15):
        new = db.News(
            title=dic['title'],
            author=dic['authors'],
            url=dic['link'],
            comments=dic['comments'],
            points=dic['points'],
            label=random.choice(('good', 'maybe', 'never'))
        )
        s.add(new)
        s.commit()
except Exception as e:
    print(e)
