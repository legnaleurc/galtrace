#-*- coding: utf-8 -*-

import re
import urllib.parse

import pyquery
import requests


def verify(uri):
    if uri.netloc == 'dl.getchu.com':
        result = urllib.parse.parse_qs(uri.query)
        if result['action'][0] == 'gdSoft':
            return 100
    return 0


def create(uri):
    link = requests.get('http://dl.getchu.com/index.php', params={
        'action': 'aa',
        'aaR18': 'true',
        'returl': uri.geturl(),
    })
    link.encoding = 'EUC-JP'
    content = link.text
    pq = pyquery.PyQuery(content)
    data = {}

    tmp = pq('a.highslide')
    thumb = tmp[0].attrib['href']
    thumb = urllib.parse.urlunsplit((uri.scheme, uri.netloc, thumb.strip(), '', ''))
    data['thumb'] = thumb

    tmp = pq('td[width="318"] div[align="left"]')
    title = tmp.text()
    data['title'] = title

    tmp = pq('td[width="318"] table td')
    vendor = tmp[3].getchildren()[0].text
    date = tmp[5].text

    data['vendor'] = vendor

    tmp = re.search(r'(\d\d\d\d)年(\d\d)月(\d\d)日', date)
    data['date'] = '/'.join(tmp.groups())

    return data
