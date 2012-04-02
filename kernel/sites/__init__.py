#! /usr/bin/env python
#-*- coding: utf-8 -*-

import urlparse, os

def __helper__( x ):
	raise RuntimeError( 'unsupported link' )
__factory__ = [ ( lambda x: 1, __helper__ ) ]

def __init__():
	plugins = map( lambda x: os.path.splitext( x )[0], filter( lambda x: x.endswith( '.py' ) and x != '__init__.py' and x != 'tests.py', os.listdir( os.path.dirname( __file__ ) ) ) )
	for plugin in plugins:
		module = None
		if __name__ == '__main__':
			module = __import__( plugin )
		else:
			module = __import__( '{0}.{1}'.format( __name__, plugin ), fromlist = [ 'verify', 'create' ] )
		__factory__.append( ( module.verify, module.create ) )

def fetch( uri ):
	uri_ = urlparse.urlsplit( uri )
	return max( __factory__, key=lambda x: x[0]( uri_ ) )[1]( uri_ )

__all__ = [ 'fetch' ]

__init__()
