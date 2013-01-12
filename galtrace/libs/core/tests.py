import json

from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import Client

from galtrace.libs.core.models import Order


class LoadTest( TestCase ):

	@classmethod
	def setUpClass( cls ):
		User.objects.create_user( username = 'alpha', password = 'alpha' )

	@classmethod
	def tearDownClass( cls ):
		User.objects.all().delete()

	def setUp( self ):
		self.url = '/load.cgi'

	def testGet( self ):
		"""
		Use GET method
		Should get failure response
		"""
		c = Client()
		response = c.get( self.url )
		self.assertEqual( response.status_code, 405 )

	def testWithoutUser( self ):
		"""
		POST without login
		Should redirect to /
		"""
		c = Client()
		response = c.post( self.url )
		self.assertRedirects( response, '/?next={0}'.format( self.url ) )

	def testEmptyArgs( self ):
		"""
		Login but empty args
		Should return JSON, success is False
		"""
		c = Client()
		result = c.login( username = 'alpha', password = 'alpha' )
		self.assertTrue( result )
		response = c.post( self.url )
		self.assertEqual( response.status_code, 200 )
		result = json.loads( response.content )
		self.assertFalse( result['success'] )

	def testWrongArgs( self ):
		"""
		Login but wrong args
		Should return JSON, success is False
		"""
		c = Client()
		result = c.login( username = 'alpha', password = 'alpha' )
		self.assertTrue( result )
		response = c.post( self.url, {
			'offset': -1,
			'limit': 0,
		} )
		self.assertEqual( response.status_code, 200 )
		result = json.loads( response.content )
		self.assertFalse( result['success'] )

	def testRightArgs( self ):
		"""
		Login and right args
		Should return JSON with data
		"""
		c = Client()
		result = c.login( username = 'alpha', password = 'alpha' )
		self.assertTrue( result )
		response = c.post( self.url, {
			'offset': 0,
			'limit': 100,
		} )
		self.assertEqual( response.status_code, 200 )
		result = json.loads( response.content )
		self.assertTrue( result['success'] )

class SaveTest( TestCase ):

	@classmethod
	def setUpClass( cls ):
		User.objects.create_user( username = 'alpha', password = 'alpha' )

	@classmethod
	def tearDownClass( cls ):
		User.objects.all().delete()
		Order.objects.all().delete()

	def setUp( self ):
		self.url = '/save.cgi'
		self.userAlpha = User.objects.get( username__exact = 'alpha' )

	def testGet( self ):
		"""
		Use GET method
		Should return failed request
		"""
		c = Client()
		response = c.get( self.url )
		self.assertEqual( response.status_code, 405 )

	def testWithoutUser( self ):
		"""
		Call without login
		Should redirect to /
		"""
		c = Client()
		response = c.post( self.url )
		self.assertRedirects( response, '/?next={0}'.format( self.url ) )

	def testEmptyArgs( self ):
		"""
		Call with empty args
		Should get a JSON which success is False
		"""
		c = Client()
		result = c.login( username = 'alpha', password = 'alpha' )
		self.assertTrue( result )
		response = c.post( self.url )
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
		response = c.post( self.url, {
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
		response = c.post( self.url, {
			'title': '1',
		} )
		self.assertEqual( response.status_code, 200 )
		result = json.loads( response.content )
		self.assertFalse( result['success'] )

	def testNonIntPhase( self ):
		"""
		Call with wrong phase
		Should get a JSON which success is False
		"""
		c = Client()
		result = c.login( username = 'alpha', password = 'alpha' )
		self.assertTrue( result )
		response = c.post( self.url, {
			'title': '1',
			'phase': 'a',
		} )
		self.assertEqual( response.status_code, 200 )
		result = json.loads( response.content )
		self.assertFalse( result['success'] )

	def testNegativePhase( self ):
		"""
		Call with wrong phase
		Should get a JSON which success is False
		"""
		c = Client()
		result = c.login( username = 'alpha', password = 'alpha' )
		self.assertTrue( result )
		response = c.post( self.url, {
			'title': '1',
			'phase': '-1',
		} )
		self.assertEqual( response.status_code, 200 )
		result = json.loads( response.content )
		self.assertFalse( result['success'] )

	def testGreaterThanFivePhase( self ):
		"""
		Call with wrong phase
		Should get a JSON which success is False
		"""
		c = Client()
		result = c.login( username = 'alpha', password = 'alpha' )
		self.assertTrue( result )
		response = c.post( self.url, {
			'title': '1',
			'phase': '6',
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
		response = c.post( self.url, {
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
		response = c.post( self.url, {
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

class DeleteTest( TestCase ):

	@classmethod
	def setUpClass( cls ):
		user = User.objects.create_user( username = 'alpha', password = 'alpha' )
		o = Order( title = 'to-be-deleted', phase = -1, volume = -1, user = user )
		o.save()

	@classmethod
	def tearDownClass( cls ):
		User.objects.all().delete()
		Order.objects.all().delete()

	def setUp( self ):
		self.url = '/delete.cgi'

	def testGet( self ):
		"""
		Call with GET
		Should return failed request
		"""
		c = Client()
		response = c.get( self.url )
		self.assertEqual( response.status_code, 405 )

	def testWithoutUser( self ):
		"""
		Call without login
		Should redirect to /
		"""
		c = Client()
		response = c.post( self.url )
		self.assertRedirects( response, '/?next={0}'.format( self.url ) )

	def testEmptyArgs( self ):
		"""
		Call with empty args
		Should return a JSON which success is False
		"""
		c = Client()
		result = c.login( username = 'alpha', password = 'alpha' )
		self.assertTrue( result )
		response = c.post( self.url )
		self.assertEqual( response.status_code, 200 )
		result = json.loads( response.content )
		self.assertFalse( result['success'] )

	def testEmptyTitle( self ):
		"""
		Call with empty title
		Should return a JSON which success is False
		"""
		c = Client()
		result = c.login( username = 'alpha', password = 'alpha' )
		self.assertTrue( result )
		response = c.post( self.url, {
			'title': '',
		} )
		self.assertEqual( response.status_code, 200 )
		result = json.loads( response.content )
		self.assertFalse( result['success'] )

	def testDeleteNonExists( self ):
		"""
		Trying to delete non-exists record
		Should return a JSON which success is False
		"""
		c = Client()
		result = c.login( username = 'alpha', password = 'alpha' )
		self.assertTrue( result )
		response = c.post( self.url, {
		} )
		self.assertEqual( response.status_code, 200 )
		result = json.loads( response.content )
		self.assertFalse( result['success'] )
		response = c.post( self.url, {
			'orders[]': 'non-exists',
		} )
		self.assertEqual( response.status_code, 200 )
		result = json.loads( response.content )
		self.assertFalse( result['success'] )

	def testRightArgs( self ):
		"""
		Trying to delete non-exists record
		Should return a JSON which success is False
		"""
		c = Client()
		result = c.login( username = 'alpha', password = 'alpha' )
		self.assertTrue( result )
		response = c.post( self.url, {
			'orders[]': 'to-be-deleted',
		} )
		self.assertEqual( response.status_code, 200 )
		result = json.loads( response.content )
		self.assertTrue( result['success'] )

class FetchTest( TestCase ):

	def setUp( self ):
		self.url = '/fetch.cgi'

	def testGet( self ):
		c = Client()
		response = c.get( self.url )
		self.assertEqual( response.status_code, 405 )

	def testWithoutUser( self ):
		c = Client()
		response = c.post( self.url )
		self.assertRedirects( response, '/?next={0}'.format( self.url ) )