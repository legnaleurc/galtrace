#-*- coding: utf-8 -*-

import re
import urllib.parse

import pyquery
import requests

from . import Site as AbstractSite


class Site(AbstractSite):

    def do_evaluate(self, uri):
        if uri.netloc == 'gyutto.com':
            return 100
        else:
            return 0

    def do_parse(self, uri):
        m = re.match(r'^/i/item(\d+)$', uri.path)
        if not m:
            raise RuntimeError('invalid url path')

        uri_ = urllib.parse.urlunsplit((uri.scheme, uri.netloc, '/adult_check.php', '', ''))
        link = requests.get(uri_, params={
            '_adult_check': 'yes',
            'item_flag': '1',
            'ref_path': uri.path,
            'id': m.group(1),
        })
        link.encoding = 'shift-jis'
        content = link.text
        pq = pyquery.PyQuery(content)

        path = pq('#naviglobal_InArea img[src*="on"]')
        category = path.attr.name

        log = []
        error = []
        tmp = pq('#RightSide div > h1')
        tmp.remove('span, img')
        title = tmp.text()
        tmp = pq('#RightSide div.unit_DetailBasicInfo dl.BasicInfo.clearfix')
        if category == 'category_6':
            vendor = pyquery.PyQuery(tmp[2]).find('dd a').text()
            date_ = pyquery.PyQuery(tmp[9]).find('dd').text()
        elif category == 'category_10':
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
