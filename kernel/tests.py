from kernel.models import Order

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

class SaveTest( TestCase ):

	def setUp( self ):
		self.saveUrl = '/save.cgi'
		self.userAlpha = User.objects.create_user( username = 'alpha', password = 'alpha' )

	def testGet( self ):
		"""
		Use GET method
		Should return failed request
		"""
		c = Client()
		response = c.get( self.saveUrl )
		self.assertEqual( response.status_code, 405 )

	def testWithoutUser( self ):
		"""
		Call without login
		Should redirect to /
		"""
		c = Client()
		response = c.post( self.saveUrl )
		self.assertEqual( response.status_code, 302 )

	def testEmptyArgs( self ):
		"""
		Call with empty args
		Should get a JSON which success is False
		"""
		c = Client()
		result = c.login( username = 'alpha', password = 'alpha' )
		self.assertTrue( result )
		response = c.post( self.saveUrl )
		self.assertEqual( response.status_code, 200 )
		result = json.loads( response.content )
		self.assertFalse( result['success'] )

	def testEmptyTitle( self ):
		"""
		Call with empty title
		Should get a JSON which success is False
		"""
		c = Client()
		result = c.login( username = 'alpha', password = 'alpha' )
		self.assertTrue( result )
		response = c.post( self.saveUrl, {
			'title': '',
		} )
		self.assertEqual( response.status_code, 200 )
		result = json.loads( response.content )
		self.assertFalse( result['success'] )

	def testEmptyOthers( self ):
		"""
		Call with title but others are empty
		Should get a JSON which success is False
		"""
		c = Client()
		result = c.login( username = 'alpha', password = 'alpha' )
		self.assertTrue( result )
		response = c.post( self.saveUrl, {
			'title': '1',
		} )
		self.assertEqual( response.status_code, 200 )
		result = json.loads( response.content )
		self.assertFalse( result['success'] )

	def testWrongPhase( self ):
		"""
		Call with wrong phase
		Should get a JSON which success is False
		"""
		c = Client()
		result = c.login( username = 'alpha', password = 'alpha' )
		self.assertTrue( result )
		response = c.post( self.saveUrl, {
			'title': '1',
			'phase': 'a',
		} )
		self.assertEqual( response.status_code, 200 )
		result = json.loads( response.content )
		self.assertFalse( result['success'] )

	def testWrongVolume( self ):
		"""
		Call with title and phase
		Should get a JSON which success is False
		"""
		c = Client()
		result = c.login( username = 'alpha', password = 'alpha' )
		self.assertTrue( result )
		response = c.post( self.saveUrl, {
			'title': '1',
			'phase': -1,
			'volume': 'a',
		} )
		self.assertEqual( response.status_code, 200 )
		result = json.loads( response.content )
		self.assertFalse( result['success'] )

	def testRightArgs( self ):
		"""
		Call with title and phase
		Should get a JSON which success is False
		"""
		c = Client()
		result = c.login( username = 'alpha', password = 'alpha' )
		self.assertTrue( result )
		response = c.post( self.saveUrl, {
			'title': '1',
			'phase': -1,
			'volume': -1,
		} )
		self.assertEqual( response.status_code, 200 )
		result = json.loads( response.content )
		self.assertTrue( result['success'] )
		result = Order.objects.get( user__exact = self.userAlpha, title__exact = '1' )
		self.assertEqual( result.phase, -1 )
		self.assertEqual( result.volume, -1 )
