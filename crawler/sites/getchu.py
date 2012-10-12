#-*- coding: utf-8 -*-

import re, urlparse, urllib, urllib2, pyquery, pycurl, StringIO

def verify( uri ):
	if uri.netloc == 'www.getchu.com':
		return 100
	else:
		return 0

def create( uri ):
	query = urlparse.parse_qs( uri.query )
	for key in query:
		query[key] = query[key][0]
	if 'gc' not in query:
		query['gc'] = 'gc'
	uri_ = urlparse.urlunsplit( ( uri.scheme, uri.netloc, uri.path, urllib.urlencode( query ), '' ) )

	link = pycurl.Curl()
	link.setopt( pycurl.URL, uri_.encode( 'utf-8' ) )
	sin = StringIO.StringIO()
	link.setopt( pycurl.WRITEFUNCTION, lambda x: sin.write( x ) )
	link.perform()
	link.close()
	content = sin.getvalue().decode( 'EUC-JP', 'replace' )
	sin.close()
	pq = pyquery.PyQuery( content )

	log = []
	title = pq( '#soft-title' ).remove( 'nobr' ).remove( '#wish' ).text()
	log.append( title )
	title = title.strip()
	return {
		'title': title,
		'vendor': pq( '#brandsite' ).text(),
		'date': pq( '#tooltip-day' ).text(),
		'log': log,
	}

if __name__ == '__main__':
	import sys
	uri = urlparse.urlsplit( sys.argv[1] )
	print create( uri )
