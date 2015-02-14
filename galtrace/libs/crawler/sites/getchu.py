#-*- coding: utf-8 -*-

import re
import urllib.parse
import urllib.request, urllib.parse, urllib.error
import urllib.request, urllib.error, urllib.parse
import io

import pycurl
import pyquery

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

    link = pycurl.Curl()
    link.setopt(pycurl.URL, uri_.encode('utf-8'))
    sin = io.StringIO()
    link.setopt(pycurl.WRITEFUNCTION, lambda x: sin.write(x))
    link.perform()
    link.close()
    content = sin.getvalue().decode('EUC-JP', 'replace')
    sin.close()
    pq = pyquery.PyQuery(content)

    log = []
    title = pq('#soft-title').remove('nobr').remove('#wish').text()
    log.append(title)
    title = title.strip()

    thumb = pq('#bannera + table a.highslide').attr.href
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
