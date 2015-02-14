#-*- coding: utf-8 -*-

import re
import urllib.request, urllib.parse, urllib.error
import urllib.request, urllib.error, urllib.parse
import http.cookiejar
import urllib.parse

def verify(uri):
    if uri.netloc == 'dl.getchu.com':
        result = urllib.parse.parse_qs(uri.query)
        if result['action'][0] == 'gdSoft':
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
            if 'title' not in data and re.search(r'imgs/pts_line_312\.gif', line):
                key = 'title'
            elif re.search(r'>ブランド：</td>', line):
                key = 'vendor'
            elif re.search(r'>登録日：</td>', line):
                key = 'date'
            elif re.search(r'summary="作品詳細"', line):
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
            m = re.search(r'>(\d\d\d\d)年(\d\d)月(\d\d)日<', line)
            if m:
                data[key] = '{0}/{1}/{2}'.format(m.group(1), m.group(2), m.group(3))
                key = None
        elif key == 'thumb':
            m = re.search(r'href="([^"]+)"', line)
            if m:
                thumb = urllib.parse.urlunsplit((uri.scheme, uri.netloc, m.group(1).strip(), '', ''))
                data[key] = thumb;
                key = None
    link.close()

    return data
