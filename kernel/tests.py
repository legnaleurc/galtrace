from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User

import json

class SimpleTest( TestCase ):

	def setUp( self ):
		User.objects.create_user( username = 'alpha', password = 'alpha' )

	def testGetLoad( self ):
		"""
		GET /load.cgi
		"""
		c = Client()
		response = c.get( '/load.cgi' )
		self.assertEqual( response.status_code, 405 )

	def testLoadWithoutUser( self ):
		"""
		POST /load.cgi
		Should redirect to /
		"""
		c = Client()
		response = c.post( '/load.cgi' )
		self.assertEqual( response.status_code, 302 )

	def testLoadWithUserWithoutArgs( self ):
		"""
		"""
		c = Client()
		result = c.login( username = 'alpha', password = 'alpha' )
		self.assertTrue( result )
		response = c.post( '/load.cgi' )
		self.assertEqual( response.status_code, 200 )
		result = json.loads( response.content )
		self.assertFalse( result['success'] )

	def testLoadWithUserWithArgs( self ):
		"""
		"""
		c = Client()
		result = c.login( username = 'alpha', password = 'alpha' )
		self.assertTrue( result )
		response = c.post( '/load.cgi', {
			'offset': 0,
			'limit': 100,
		} )
		self.assertEqual( response.status_code, 200 )
		result = json.loads( response.content )
		self.assertTrue( result['success'] )
