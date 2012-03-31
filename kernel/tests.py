from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User

import json

class LoadTest( TestCase ):

	def setUp( self ):
		self.loadUrl = '/load.cgi'
		User.objects.create_user( username = 'alpha', password = 'alpha' )

	def testGet( self ):
		"""
		Use GET method
		Should get failure response
		"""
		c = Client()
		response = c.get( self.loadUrl )
		self.assertEqual( response.status_code, 405 )

	def testWithoutUser( self ):
		"""
		POST without login
		Should redirect to /
		"""
		c = Client()
		response = c.post( self.loadUrl )
		self.assertEqual( response.status_code, 302 )

	def testWithUserEmptyArgs( self ):
		"""
		Login but empty args
		Should return JSON, success is False
		"""
		c = Client()
		result = c.login( username = 'alpha', password = 'alpha' )
		self.assertTrue( result )
		response = c.post( self.loadUrl )
		self.assertEqual( response.status_code, 200 )
		result = json.loads( response.content )
		self.assertFalse( result['success'] )

	def testWithUserWrongArgs( self ):
		"""
		Login but wrong args
		Should return JSON, success is False
		"""
		c = Client()
		result = c.login( username = 'alpha', password = 'alpha' )
		self.assertTrue( result )
		response = c.post( self.loadUrl, {
			'offset': -1,
			'limit': 0,
		} )
		self.assertEqual( response.status_code, 200 )
		result = json.loads( response.content )
		self.assertFalse( result['success'] )

	def testWithUserRightArgs( self ):
		"""
		Login and right args
		Should return JSON with data
		"""
		c = Client()
		result = c.login( username = 'alpha', password = 'alpha' )
		self.assertTrue( result )
		response = c.post( self.loadUrl, {
			'offset': 0,
			'limit': 100,
		} )
		self.assertEqual( response.status_code, 200 )
		result = json.loads( response.content )
		self.assertTrue( result['success'] )
