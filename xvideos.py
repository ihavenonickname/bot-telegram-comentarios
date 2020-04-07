#!/usr/bin/python3

import html
import re
import random
import json
import requests
from bs4 import BeautifulSoup

PATTERN = re.compile(r'/video(\d+)/.*')

def _fetch_page(page_number):
    url = 'https://www.xvideos.com/porn/portugues/' + str(page_number)
    res = requests.get(url)

    if res.status_code != 200:
        raise Exception('Response Error: ' + str(res.status_code))

    return BeautifulSoup(res.text, 'html.parser')

def _find_videos(soup):
    for element in soup.select('.thumb-block > .thumb-under > p > a'):
        try:
            reference = PATTERN.match(element['href']).group(1)
        except AttributeError:
            pass

        yield element['title'], reference, element['href']

def _get_comments(video_ref):
    url_mask = 'https://www.xvideos.com/threads/video-comments/get-posts/top/{0}/0/0'
    url = url_mask.format(video_ref)
    res = requests.post(url)

    if res.status_code != 200:
        raise Exception('Response Error: ' + str(res.status_code))

    json_obj = json.loads(res.text)['posts']
    json_obj = json_obj['posts']

    try:
        for attr, val in json_obj.items():
            content = html.unescape(val['message'])
            author = html.unescape(val['name'])
            if '<a href=' not in content:
                yield author, content
    except (AttributeError, IndexError) as e:
        raise IndexError

def choose_random_porn_comment():
    for _ in range(10):
        page = _fetch_page(random.randint(1, 40))
        videos = _find_videos(page)

        try:
            title, reference, url = random.choice(list(videos))
            comments = _get_comments(reference)
            author, content = random.choice(list(comments))
        except IndexError:
            continue

        return author, content, title, url

    raise Exception('Too hard')

def _fetch_tag_page(page_number, tag):
    if tag is not None:
        url = 'https://www.xvideos.com/?k='+ str(tag) +'&p=' + str(page_number)
    else:
        url = 'https://www.xvideos.com/new/' + str(page_number)

    res = requests.get(url)
    if res.status_code != 200:
        raise Exception('Response Error: ' + str(res.status_code))

    return BeautifulSoup(res.text, 'html.parser')

def choose_random_video(tag=None):
    for _ in range(10):
        page = _fetch_tag_page(random.randint(1, 4), tag)
        videos = _find_videos(page)

        try:
            title, reference, url = random.choice(list(videos))
            url = 'https://xvideos.com'+url
            return url
        except IndexError:
            raise Exception('Response Error: Bad search term')

    raise Exception('Too hard')

def main():
    # comment = choose_random_porn_comment()
    # print(*comment, sep='\n')

    video = choose_random_video()
    print(video, sep='\n')

if __name__ == '__main__':
    main()
