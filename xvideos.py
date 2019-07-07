#!/usr/bin/python3

import re
import random
import json
from html import unescape
from collections import namedtuple

import requests
from bs4 import BeautifulSoup

class XvideosException(Exception):
    pass

Comment = namedtuple('Comment', ['author', 'content', 'datediff', 'country', 'score'])

PATTERN = re.compile(r'/video(\d+)/.*')
N_ATTEMPTS = 5

def _fetch_page(url):
    res = requests.get(url)

    if res.status_code != 200:
        raise Exception(f'Response Error: {res.status_code}')

    return BeautifulSoup(res.text, 'html.parser')

def _find_videos(soup):
    result = []

    for element in soup.select('.thumb-block > div > p > a'):
        try:
            reference = PATTERN.match(element['href']).group(1)
        except AttributeError:
            pass

        result.append(reference)

    return result

def _get_comments(video_ref):
    url_mask = 'https://www.xvideos.com/video-get-comments/{0}/0/'
    url_mask = 'https://www.xvideos.com/threads/video-comments/get-posts/top/{0}/0/0'
    url = url_mask.format(video_ref)
    res = requests.post(url)

    if res.status_code != 200:
        raise Exception('Response Error: ' + str(res.status_code))

    posts = json.loads(res.text)['posts']

    if posts['nb_posts_total'] < 1:
        return

    def get_safe(prop):
        x = item.get(prop, '')
        return unescape(x) if x and isinstance(x, str) else None

    result = []

    for item in posts['posts'].values():
        try:
            score = item['votes']['nb'] - item['votes']['nbb']
        except (KeyError, TypeError):
            score = 0

        comment = Comment(
            get_safe('name') or 'Unknown user',
            get_safe('message'),
            get_safe('time_diff') or 'some time ago',
            get_safe('country_name') or 'unknown region',
            score
        )

        result.append(comment)

    return result

def choose_random_porn_comment(search_term=None):
    for _ in range(N_ATTEMPTS):
        r = random.randint(1, 10)

        if search_term:
           url = f'https://www.xvideos.com/?k={search_term}&p={r}'
        else:
            url = f'https://www.xvideos.com/'

        page = _fetch_page(url)
        references = _find_videos(page)

        if not references:
            msg = 'No videos were found'
            if search_term:
                msg += f' with search term "{search_term}"'
            raise XvideosException(msg + '. :(')

        comments = _get_comments(random.choice(references))

        if not comments:
            continue

        return random.choice(comments)

    raise XvideosException(f'No comments were found after {N_ATTEMPTS} attempts. :(')

def main():
    comment = choose_random_porn_comment()
    print(comment)
    print()

if __name__ == '__main__':
    main()

