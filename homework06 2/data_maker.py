import db
import scraputils as su
from random import choice

s = db.session()

for dic in su.get_news(n_pages=3):
    try:
        new = db.News(
            title=dic['title'],
            author=dic['authors'],
            url=dic['link'],
            comments=dic['comments'],
            points=dic['points'],
            label=choice(('good', 'maybe', 'never'))
            )
        s.add(new)
        s.commit()
    except Exception as e:
        print(e)
