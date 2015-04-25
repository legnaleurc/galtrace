#-*- coding: utf-8 -*-

import re
import urllib.parse
import urllib.request

import pyquery

from . import Site as AbstractSite


class Site(AbstractSite):

    def do_evaluate(self, uri):
        if uri.netloc == 'www.dlsite.com':
            return 100
        else:
            return 0

    def do_parse(self, uri):
        uri_ = urllib.parse.urlunsplit((uri.scheme, uri.netloc, uri.path, '', ''))
        link = urllib.request.urlopen(uri_)
        content = link.read().decode('utf-8', 'replace')
        link.close()
        pq = pyquery.PyQuery(content)

        log = []
        title = pq('#work_name').remove('span').text()
        vendor = pq('#work_maker span.maker_name a').text()
        date = pq('#work_outline').text()
        thumb = pq('#work_visual').attr.style

        m = re.search(r'販売日.: (\d\d\d\d)年(\d{1,2})月(\d{1,2})日', date)
        date = '{0}/{1:02d}/{2:02d}'.format(m.group(1), int(m.group(2)), int(m.group(3)))

        m = re.search(r'url\(([^)]+)\)', thumb)
        thumb = m.group(1)

        return {
            'title': title,
            'vendor': vendor,
            'date': date,
            'thumb': 'http:' + thumb,
            'log': log,
        }
