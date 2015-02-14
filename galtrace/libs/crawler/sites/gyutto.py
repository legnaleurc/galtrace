#-*- coding: utf-8 -*-

import re
import urllib.parse
import urllib.request, urllib.error, urllib.parse
import http.cookiejar
import urllib.request, urllib.parse, urllib.error

import pyquery

def verify(uri):
    if uri.netloc == 'gyutto.com':
        return 100
    else:
        return 0

def create(uri):
    m = re.match(r'^/i/item(\d+)$', uri.path)
    if not m:
        raise RuntimeError('invalid url path')
    query = {
        '_adult_check': 'yes',
        'item_flag': '1',
        'ref_path': uri.path,
        'id': m.group(1),
    }

    uri_ = urllib.parse.urlunsplit((uri.scheme, uri.netloc, '/adult_check.php', '', ''))
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))
    link = opener.open(uri_, urllib.parse.urlencode(query))
    content = link.read().decode('shift-jis', 'replace')
    link.close()

    pq = pyquery.PyQuery(content)

    path = pq('#topicpath a')
    category = path[2].text

    log = []
    error = []
    tmp = pq('#RightSide div > h1')
    tmp.remove('span, img')
    title = tmp.text()
    tmp = pq('#RightSide div.unit_DetailBasicInfo dl.BasicInfo.clearfix')
    if category == '美少女ゲーム':
        vendor = pyquery.PyQuery(tmp[2]).find('dd a').text()
        date_ = pyquery.PyQuery(tmp[9]).find('dd').text()
    elif category == '同人ソフト':
        vendor = pyquery.PyQuery(tmp[2]).find('dd a')[0].text
        date_ = pyquery.PyQuery(tmp[5]).find('dd').text()
    else:
        date_ = ''
    m = re.match(r'^(\d\d\d\d)年(\d\d)月(\d\d)日$', date_)
    if not m:
        error.append('invalid date')
        date_ = ''
    else:
        date_ = '{0}/{1}/{2}'.format(m.group(1), m.group(2), m.group(3))
    thumb = pq('#noMovie a.highslide').attr.href.strip()
    thumb = urllib.parse.urlunsplit((uri.scheme, uri.netloc, thumb, '', ''))

    return {
        'title': title,
        'vendor': vendor,
        'date': date_,
        'thumb': thumb,
        'log': log,
        'error': error,
    }

if __name__ == '__main__':
    import sys
    print(create(urllib.parse.urlsplit(sys.argv[1])))
    sys.exit(0)
