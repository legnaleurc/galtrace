#! /usr/bin/env python
#-*- coding: utf-8 -*-

import re, urlparse, urllib, urllib2, pyquery

def verify( uri ):
	if uri.netloc == 'www.getchu.com':
		return 100
	else:
		return 0

def create( uri ):
	query = urlparse.parse_qs( uri.query )
	for key in query:
		query[key] = query[key][0]
	if( 'gc' not in query ):
		query['gc'] = 'gc'
	uri_ = urlparse.urlunsplit( ( uri.scheme, uri.netloc, uri.path, urllib.urlencode( query ), '' ) )

	link = urllib2.urlopen( uri_ )
	content = link.read().decode( 'EUC-JP', 'replace' )
	link.close()
	pq = pyquery.PyQuery( content )

	log = []
	title = pq( '#soft-title' ).remove( 'nobr' ).remove( '#wish' ).text()
	log.append( title )
	title = title.strip()
	return { 'title': title, 'vendor': pq( '#brandsite' ).text(), 'date': pq( '#tooltip-day' ).text(), 'log': log }

if __name__ == '__main__':
	import sys
	uri = urlparse.urlsplit( sys.argv[1] )
	print create( uri )
