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
        df.to_csv('blogs.csv', index=False)
    return df



def get_articles():
    try:    
        df = pd.read_csv('articles.csv')
    except FileNotFoundError:
        url = 'https://inshorts.com/en/read'
        response = get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        categories = [li.text.lower() for li in soup.select('li')][1:]
        categories[0] = 'national'

        inshorts = []

        for category in categories:

            url = 'https://inshorts.com/en/read' + '/' + category
            response = get(url)
            soup = BeautifulSoup(response.content, 'html.parser')

            titles = [span.text for span in soup.find_all('span', itemprop='headline')]
            contents = [div.text for div in soup.find_all('div', itemprop='articleBody')]

            for i in range(len(titles)):

                article = {
                    'title': titles[i],
                    'content': contents[i],
                    'category': category,
                }

                inshorts.append(article)
    return df
