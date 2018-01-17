#!/usr/bin/python3

import sys
from html.parser import HTMLParser
from html import unescape
import re
import random
import json
import requests
from bs4 import BeautifulSoup

def _get_videos_on_page(page_number):
    url = 'https://www.xvideos.com/porn/portugues/' + str(page_number)

    res = requests.get(url)

    if res.status_code != 200:
        raise Exception('Response Error: ' + str(res.status_code))

    soup = BeautifulSoup(res.text, 'html.parser')
    pattern = re.compile(r'/video(\d+)/.*')

    elements = []
    try:
        for element in soup.select('.thumb-block > p > a'):
            try:
                elements.append({
                    'reference': pattern.match(element['href']).group(1),
                    'title': element['title']
                })
            except Exception:
                pass
    except Exception as e:
        print(e)

        return []

    return elements

def _get_comments(video_reference):
    url_mask = 'https://www.xvideos.com/video-get-comments/{0}/0/'
    url = url_mask.format(video_reference)

    res = requests.post(url)

    if res.status_code != 200:
        raise Exception('Response Error: ' + str(res.status_code))

    comments = []

    for item in json.loads(res.text)['comments']:
        content = unescape(item['c']).replace('<br />', '\n')

        if '<a href=' in content:
            continue

        comments.append({
            'author': unescape(item['n']),
            'content': content,
            'video': 'https://www.xvideos.com/video{0}/'.format(video_reference)
        })

    return comments

def choose_random_porn_comment():
    while True:
        videos = _get_videos_on_page(random.randint(1, 41))
        video = random.choice(videos)

        comments = _get_comments(video['reference'])

        try:
            comment = random.choice(comments)
        except IndexError:
            continue

        return {
            'author': comment['author'],
            'content': comment['content'],
            'title': video['title']
        }

def main():
    comment = choose_random_porn_comment()

    print(comment['author'])
    print(comment['content'])

if __name__ == '__main__':
    main()

