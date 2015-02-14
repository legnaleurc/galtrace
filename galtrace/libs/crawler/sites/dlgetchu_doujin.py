#-*- coding: utf-8 -*-

import re
import urllib.request, urllib.parse, urllib.error
import urllib.request, urllib.error, urllib.parse
import http.cookiejar
import urllib.parse

def verify(uri):
    if uri.netloc == 'dl.getchu.com':
        result = urllib.parse.parse_qs(uri.query)
        if result['action'][0] == 'gd':
            return 100
    return 0

def create(uri):
    query = {}
    query['action'] = 'aa'
    query['aaR18'] = 'true'
    query['returl'] = uri.geturl()

    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
    link = opener.open('http://dl.getchu.com/index.php', urllib.parse.urlencode(query))
    data = {}
    key = None
    for line in link:
        line = line.decode('EUC-JP', 'replace')
        if not key:
            if re.search(r'images/shosai_tl_new\.gif', line):
                key = 'title'
            elif re.search(r'>サークル</td>', line):
                key = 'vendor'
            elif re.search(r'>登録日</td>', line):
                key = 'date'
            elif re.search(r'>作品詳細<', line):
                key = 'thumb'
        elif key == 'title':
            m = re.search(r'<div.+>(.+)</div>', line)
            if m:
                data[key] = m.group(1)
                key = None
        elif key == 'vendor':
            m = re.search(r'<a.+>(.+)</a>', line)
            if m:
                data[key] = m.group(1)
                key = None
        elif key == 'date':
            m = re.search(r'>(.+)</td>', line)
            if m:
                data[key] = m.group(1)
                key = None
        elif key == 'thumb':
            m = re.search(r'<img src="([^"]+)"[^>]*>', line)
            if m:
                thumb = urllib.parse.urlunsplit((uri.scheme, uri.netloc, m.group(1).strip(), '', ''))
                data[key] = thumb
                key = None
    link.close()

    return data
