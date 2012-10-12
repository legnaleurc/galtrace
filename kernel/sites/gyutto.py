#! /usr/bin/env python
#-*- coding: utf-8 -*-

import re, urlparse, urllib2, cookielib, urllib, pyquery

def verify( uri ):
	if uri.netloc == 'gyutto.com':
		return 100
	else:
		return 0

def create( uri ):
	m = re.match( r'^/i/item(\d+)$', uri.path )
	if not m:
		# TODO error
		pass
	query = {
		'_adult_check': 'yes',
		'item_flag': '1',
		'ref_path': uri.path,
		'id': m.group( 1 ),
	}

	uri_ = urlparse.urlunsplit( ( uri.scheme, uri.netloc, '/adult_check.php', '', '' ) )
	opener = urllib2.build_opener( urllib2.HTTPCookieProcessor( cookielib.CookieJar() ) )
	link = opener.open( uri_, urllib.urlencode( query ) )
	content = link.read().decode( 'shift-jis', 'replace' )
	link.close()

	pq = pyquery.PyQuery( content )

	log = []
	error = []
	tmp = pq( '#RightSide div > h1' )
	tmp.remove( 'span, img' )
	title = tmp.text()
	tmp = pq( '#RightSide div.unit_DetailBasicInfo dl.BasicInfo.clearfix' )
	vendor = pyquery.PyQuery( tmp[2] ).find( 'dd a' ).text()
	date_ = pyquery.PyQuery( tmp[9] ).find( 'dd' ).text()
	m = re.match( ur'^(\d\d\d\d)年(\d\d)月(\d\d)日$', date_ )
	if not m:
		error.append( 'invalid date' )
		date_ = u''
	else:
		date_ = u'{0}/{1}/{2}'.format( m.group( 1 ), m.group( 2 ), m.group( 3 ) )

	return {
		'title': title,
		'vendor': vendor,
		'date': date_,
		'log': log,
		'error': error,
	}

if __name__ == '__main__':
	import sys
	print create( urlparse.urlsplit( sys.argv[1] ) )
	sys.exit( 0 )
