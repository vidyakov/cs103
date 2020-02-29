import requests
from bs4 import BeautifulSoup
import re


def extract_news(parser):
    """ Extract news from a given web page """
    news_list = []

    title = [title.text for title in parser.find_all(class_='storylink')]
    link = [link['href'] for link in parser.find_all(class_='storylink')]
    points = [int(point.text.split()[0]) for point in parser.find_all(class_='score')]
    authors = [author.text for author in parser.find_all(class_='hnuser')]
    comments = [int(comment.split('\xa0')[0]) if comment != 'discuss' else 0
                for comment in parser.find_all(string=(re.compile('[0-9]+\xa0comments$'),
                                                       re.compile('^discuss$')))]

    for new in zip(title, link, points, authors, comments):
        news_list.append({
            'title': new[0],
            'link': new[1],
            'points': new[2],
            'authors': new[3],
            'comments': new[4]
        })

    return news_list


def extract_next_page(parser):
    """ Extract next page URL """
    return parser.find(class_='morelink')['href']


def get_news(url="https://news.ycombinator.com/", n_pages=1):
    """ Collect news from a given web page """
    news = []
    while n_pages:
        print("Collecting data from page: {}".format(url))
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        news_list = extract_news(soup)
        next_page = extract_next_page(soup)
        url = "https://news.ycombinator.com/" + next_page
        news.extend(news_list)
        n_pages -= 1
    return news
