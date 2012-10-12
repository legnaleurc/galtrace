import sys, pkgutil

def __module_filter():
	for importer, name, isPackage in pkgutil.walk_packages( sys.modules[__name__].__path__ ):
		if not isPackage:
			loader = importer.find_module( name )
			module = loader.load_module( name )
			yield module

def __helper( x ):
	raise RuntimeError( u'unsupported link' )
factory = [ ( lambda x: 1, __helper ) ]

for module in __module_filter():
	factory.append( ( module.verify, module.create ) )
