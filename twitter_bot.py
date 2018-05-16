#!/usr/bin/env python2
# -*- coding: utf-8 -*-


import tweepy
import HTMLParser
import re
import random
import json
import requests
from bs4 import BeautifulSoup


#inserir seus dados do twitter aqui
consumer_key = "consumer key"
consumer_secret = "consumer secret"
access_token = "access token"
access_token_secret = "access token secret"


#faz a autenticacao e login aqui
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

user = api.me()


PATTERN = re.compile(r'/video(\d+)/.*')

#encontra a pagina
def _fetch_page(page_number):
    url = 'https://www.xvideos.com/porn/portugues/' + str(page_number)
    res = requests.get(url)

    if res.status_code != 200:
        raise Exception('Response Error: ' + str(res.status_code))

    return BeautifulSoup(res.text, 'html.parser')

#encontra os videos
def _find_videos(soup):
    for element in soup.select('.thumb-block > p > a'):
        try:
            reference = PATTERN.match(element['href']).group(1)
        except AttributeError:
            pass

        yield element['title'], reference

#encontra os comentarios
def _get_comments(video_ref):
    url_mask = 'https://www.xvideos.com/video-get-comments/{0}/0/'
    url = url_mask.format(video_ref)
    res = requests.post(url)

    if res.status_code != 200:
        raise Exception('Response Error: ' + str(res.status_code))

    for item in json.loads(res.text)['comments']:
        content = HTMLParser.HTMLParser().unescape(item['c']).replace('<br />', '\n')
        author = HTMLParser.HTMLParser().unescape(item['n'])

        if '<a href=' not in content:
            yield author, content

#escolhe um comentario aleatorio
def choose_random_porn_comment():
    for _ in range(10):
        page = _fetch_page(random.randint(1, 40))
        videos = _find_videos(page)
        title, reference = random.choice(list(videos))
        comments = _get_comments(reference)

        try:
            author, content = random.choice(list(comments))
        except IndexError:
            continue

        return author, content, title

    raise Exception('Too hard')


def main():
    #comentario aleatorio = comment
    comment = choose_random_porn_comment()

    #printa o comentario no terminal
    print(format_comment(*comment))
    
    #formata o comentario
    comentarioo = format_comment(*comment)
    
    #posta no twitter
    api.update_status(comentarioo)
    
#funcao para formatar o comentario    
def format_comment(author, content, title):
    mask = '{0} comentou o seguinte:\n{1}\n\nVi isso no video:\n{2}'

    author = author.encode('utf-8')
    content = content.encode('utf-8')
    title = title.encode('utf-8')
    return mask.format(author, content, title)

if __name__ == '__main__':
    main()