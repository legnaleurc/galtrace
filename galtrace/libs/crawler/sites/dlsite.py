#-*- coding: utf-8 -*-

import re
import urllib.parse
import urllib.request, urllib.error, urllib.parse

import pyquery

def verify(uri):
    if uri.netloc == 'www.dlsite.com':
        return 100
    else:
        return 0

def create(uri):
    uri_ = urllib.parse.urlunsplit((uri.scheme, uri.netloc, uri.path, '', ''))
    link = urllib.request.urlopen(uri_)
    content = link.read().decode('utf-8', 'replace')
    link.close()
    pq = pyquery.PyQuery(content)

    log = []
    title = pq('#work_name').text()
    vendor = pq('#work_maker span.maker_name a').text()
    date_ = pq('#work_outline').text()
    thumb = pq('#work_visual img').attr.src.strip()

    m = re.search(r'販売日.: (\d\d\d\d)年(\d{1,2})月(\d{1,2})日', date_)
    date_ = '{0}/{1:02d}/{2:02d}'.format(m.group(1), int(m.group(2)), int(m.group(3)))

    return {
        'title': title,
        'vendor': vendor,
        'date': date_,
        'thumb': 'http:' + thumb,
        'log': log,
    }
