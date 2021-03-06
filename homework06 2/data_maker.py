import db
import scraputils as su

s = db.session()

for dic in su.get_news(n_pages=14):
    try:
        new = db.News(
            title=dic['title'],
            author=dic['authors'],
            url=dic['link'],
            comments=dic['comments'],
            points=dic['points']
            )
        s.add(new)
        s.commit()
    except Exception as e:
        print(e)
