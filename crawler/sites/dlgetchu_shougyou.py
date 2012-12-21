#-*- coding: utf-8 -*-

import re
import urllib
import urllib2
import cookielib
import urlparse

def verify( uri ):
	if uri.netloc == 'dl.getchu.com':
		result = urlparse.parse_qs( uri.query )
		if result['action'][0] == 'gdSoft':
			return 100
	return 0

def create( uri ):
	query = {}
	query['action'] = 'aa'
	query['aaR18'] = 'true'
	query['returl'] = uri.geturl()

	opener = urllib2.build_opener( urllib2.HTTPCookieProcessor( cookielib.CookieJar() ) )
	link = opener.open( 'http://dl.getchu.com/index.php', urllib.urlencode( query ) )
	data = {}
	key = None
	for line in link:
		line = line.decode( 'EUC-JP', 'replace' )
		if not key:
			if 'title' not in data and re.search( ur'imgs/pts_line_312\.gif', line ):
				key = 'title'
			elif re.search( ur'>ブランド：</td>', line ):
				key = 'vendor'
			elif re.search( ur'>登録日：</td>', line ):
				key = 'date'
		elif key == 'title':
			m = re.search( ur'<div.+>(.+)</div>', line )
			if m:
				data[key] = m.group( 1 )
				key = None
		elif key == 'vendor':
			m = re.search( ur'<a.+>(.+)</a>', line )
			if m:
				data[key] = m.group( 1 )
				key = None
		elif key == 'date':
			m = re.search( ur'>(\d\d\d\d)年(\d\d)月(\d\d)日<', line )
			if m:
				data[key] = '{0}/{1}/{2}'.format( m.group( 1 ), m.group( 2 ), m.group( 3 ) )
				key = None
	link.close()

	return data