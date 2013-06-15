from django.conf import settings
from django.template import Library
from django.contrib.staticfiles.templatetags.staticfiles import StaticFilesNode, static
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
			rel = u'stylesheet/less'
		else:
			rel = u'stylesheet'
			try:
				from less.templatetags.less import less
			except ImportError:
				less = lambda path: u''
			path = self.path.resolve( context )
			path = less( path )
			lessPath = static( path )
		return format_html( u'<link rel="{0}" type="text/css" href="{1}" />', rel, lessPath )


@register.tag
def less_script( parser, token ):
	return LessScript.handle_token( parser, token )

@register.tag
def less_file( parser, token ):
	return LessFile.handle_token( parser, token )
