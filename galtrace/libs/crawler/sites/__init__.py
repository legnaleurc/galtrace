#-*- coding: utf-8 -*-

import pkgutil
import sys


class _UnsupportedLinkError( RuntimeError ):
	pass


def _module_filter():
	for importer, name, isPackage in pkgutil.walk_packages( sys.modules[__name__].__path__ ):
		if not isPackage:
			loader = importer.find_module( name )
			module = loader.load_module( name )
			yield module

def _helper( x ):
	raise _UnsupportedLinkError( u'unsupported link' )
factory = [ ( lambda x: 1, _helper ) ]

for module in _module_filter():
	factory.append( ( module.verify, module.create ) )
