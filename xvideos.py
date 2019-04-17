#!/usr/bin/python3

from html import unescape
import re
import random
import json
import requests
from bs4 import BeautifulSoup

class XvideosException(Exception):
    pass

PATTERN = re.compile(r'/video(\d+)/.*')

def _fetch_page(url):
    res = requests.get(url)

    if res.status_code != 200:
        raise Exception(f'Response Error: {res.status_code}')

    return BeautifulSoup(res.text, 'html.parser')

def _find_videos(soup):
    for element in soup.select('.thumb-block > div > p > a'):
        try:
            reference = PATTERN.match(element['href']).group(1)
        except AttributeError:
            pass

        yield element['title'], reference

def _get_comments(video_ref):
    url_mask = 'https://www.xvideos.com/video-get-comments/{0}/0/'
    url_mask = 'https://www.xvideos.com/threads/video-comments/get-posts/top/{0}/0/0'
    url = url_mask.format(video_ref)
    res = requests.post(url)

    if res.status_code != 200:
        raise Exception('Response Error: ' + str(res.status_code))

    comments = json.loads(res.text)['posts']['posts'].values()
    for comment in comments:
        author = unescape(comment['name'])
        content = unescape(comment['message'])

        datediff = comment['time_diff']

        if comment['country_name']:
            country = comment['country_name'].strip()
        else:
            country = ''

        yield author, content, country, datediff

def choose_random_porn_comment(search_term=None):
    for _ in range(5):
        r = random.randint(1, 10)

        if search_term:
           url = f'https://www.xvideos.com/?k={search_term}&p={r}'
        else:
            url = f'https://www.xvideos.com/porn/portugues/{r}'

        page = _fetch_page(url)
        videos = _find_videos(page)

        try:
            title, reference = random.choice(list(videos))
        except IndexError:
            raise XvideosException('No video found')

        comments = _get_comments(reference)

        try:
            author, content, country, datediff = random.choice(list(comments))
        except IndexError:
            continue

        return author, content, country, datediff, title

    raise XvideosException('No comment found')

def main():
    comment = choose_random_porn_comment('creampie')
    print(*comment, sep='\n')
    print()

if __name__ == '__main__':
    main()

