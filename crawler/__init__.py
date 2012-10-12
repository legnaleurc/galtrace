#-*- coding: utf-8 -*-

import urlparse
import sites

def fetch( uri ):
	uri_ = urlparse.urlsplit( uri )
	return max( sites.factory, key=lambda x: x[0]( uri_ ) )[1]( uri_ )

__all__ = [ 'fetch' ]
