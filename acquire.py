from requests import get
from bs4 import BeautifulSoup as b

import pandas as pd
import numpy as np


def get_blogs():
    try:    
        df = pd.read_csv('blogs.csv')
    except FileNotFoundError:
        url = 'https://codeup.com/blog/'
        headers = {'User-Agent': 'Codeup Data Science'} # Some websites don't accept the pyhon-requests default user-agent
        response = get(url, headers=headers)
        soup = b(response.content, 'html.parser')
        divs = soup.find_all('div', class_='post-content')
        links = []
        for div in divs:
            links.append(div.find('a')['href'])
        blogs = []
        for link in links:
            blog = {}
            response = get(link, headers=headers)
            title = soup.find('h2').text
            p = soup.find_all('p')[4].text
            blog.update({'title': title})
            blog.update({'content': p})
            blogs.append(blog)
        df = pd.DataFrame(blogs)
    return df



def get_articles():
    try:    
        df = pd.read_csv('articles.csv')
    except FileNotFoundError:
        topics = ['business', 'sports', 'technology', 'entertainment']
        articles = []
        for topic in topics:
            article={}
            url = f'https://inshorts.com/en/read/{topic}'
            response = get(url)
            soup = b(response.content, 'html.parser')
            title =soup.find_all('span', itemprop='headline')[0].text
            content = soup.find_all('div', itemprop='articleBody')[0].text
            content = content.replace('\n', '')
            article.update({'title': title})
            article.update({'content': content})
            articles.append(article)
        df = pd.DataFrame(articles)
        return df
