#-*- coding: utf-8 -*-

import re
import urllib.parse
import io

import pyquery
import requests


def verify(uri):
    if uri.netloc == 'www.getchu.com':
        return 100
    else:
        return 0

def create(uri):
    query = urllib.parse.parse_qs(uri.query)
    for key in query:
        query[key] = query[key][0]
    if 'gc' not in query:
        query['gc'] = 'gc'
    uri_ = urllib.parse.urlunsplit((uri.scheme, uri.netloc, uri.path, urllib.parse.urlencode(query), ''))

    link = requests.get(uri_)
    link.encoding = 'EUC-JP'
    content = link.text
    pq = pyquery.PyQuery(content)

    log = []
    title = pq('#soft-title').remove('nobr').remove('#wish').text()
    log.append(title)
    title = title.strip()

    thumb = pq('#soft_table a.highslide').attr.href
    log.append(thumb)
    if not thumb:
        thumb = ''
    else:
        thumb = urllib.parse.urlunsplit((uri.scheme, uri.netloc, thumb.strip(), '', ''))
    log.append(thumb)

    return {
        'title': title,
        'vendor': pq('#brandsite').text(),
        'date': pq('#tooltip-day').text(),
        'thumb': thumb,
        'log': log,
    }

if __name__ == '__main__':
    import sys
    uri = urllib.parse.urlsplit(sys.argv[1])
    print(create(uri))
