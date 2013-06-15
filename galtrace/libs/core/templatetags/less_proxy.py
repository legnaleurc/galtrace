from django.conf import settings
from django.template import Library
from django.contrib.staticfiles.templatetags.staticfiles import StaticFilesNode
from django.utils.html import format_html


register = Library()
DEV_MODE = settings.DEBUG


class LessScript( StaticFilesNode ):

	def __init__( self, varname = None, path = None ):
		StaticFilesNode.__init__( self, varname, path )

	def render( self, context ):
		if not DEV_MODE:
			return u''
		lessPath = StaticFilesNode.render( self, context )
		return format_html( u'<script src="{0}"></script>', lessPath )

class LessFile( StaticFilesNode ):

	def __init__( self, varname = None, path = None ):
		StaticFilesNode.__init__( self, varname, path )

	def render( self, context ):
		if DEV_MODE:
			lessPath = StaticFilesNode.render( self, context )
		else:
			from less.templatetags.less import less
			path = self.path.resolve( context )
			lessPath = less( path )
		return format_html( u'<link rel="stylesheet/less" type="text/css" href="{0}" />', lessPath )


@register.tag
def less_script( parser, token ):
	return LessScript.handle_token( parser, token )

@register.tag
def less_file( parser, token ):
	return LessFile.handle_token( parser, token )
