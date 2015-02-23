import json

from django.contrib.auth.models import User
from django.test import TestCase
from django.test.client import Client

from galtrace.libs.core.models import Order


class LoadTest(TestCase):

    @classmethod
    def setUpClass(cls):
        User.objects.create_user(username = 'alpha', password = 'alpha')

    @classmethod
    def tearDownClass(cls):
        User.objects.all().delete()

    def setUp(self):
        self.url = '/load.cgi'

    def testGet(self):
        """
        Use GET method
        Should get failure response
        """
        c = Client()
        response = c.get(self.url)
        self.assertEqual(response.status_code, 405)

    def testEmptyArgs(self):
        """
        Login but empty args
        Should return JSON, success is False
        """
        c = Client()
        result = c.login(username = 'alpha', password = 'alpha')
        self.assertTrue(result)
        response = c.post(self.url)
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.content.decode('utf-8'))
        self.assertFalse(result['success'])

    def testWrongArgs(self):
        """
        Login but wrong args
        Should return JSON, success is False
        """
        c = Client()
        result = c.login(username = 'alpha', password = 'alpha')
        self.assertTrue(result)
        response = c.post(self.url, {
            'offset': -1,
            'limit': 0,
        })
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.content.decode('utf-8'))
        self.assertFalse(result['success'])

    def testRightArgs(self):
        """
        Login and right args
        Should return JSON with data
        """
        c = Client()
        result = c.login(username = 'alpha', password = 'alpha')
        self.assertTrue(result)
        response = c.post(self.url, {
            'user_id': 'alpha',
            'offset': 0,
            'limit': 100,
            'phase': 0,
        })
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.content.decode('utf-8'))
        self.assertTrue(result['success'])

class SaveTest(TestCase):

    @classmethod
    def setUpClass(cls):
        user = User.objects.create_user(username = 'alpha', password = 'alpha')
        order = Order(user=user, title = 'test_title', uri = 'test_uri', vendor = 'test_vendor', date = '1234/56/78', phase=0, volume = -1)
        order.save()
        user = User.objects.create_user(username = 'beta', password = 'beta')
        order = Order(user=user, title = 'test_title', uri = 'test_uri', vendor = 'test_vendor', date = '1234/56/78', phase=0, volume = -1)
        order.save()

    @classmethod
    def tearDownClass(cls):
        User.objects.all().delete()
        Order.objects.all().delete()

    def setUp(self):
        self.url = '/save.cgi'
        self.userAlpha = User.objects.get(username__exact = 'alpha')
        self.userBeta = User.objects.get(username__exact = 'beta')

    def testGet(self):
        """
        Use GET method
        Should return failed request
        """
        c = Client()
        response = c.get(self.url)
        self.assertEqual(response.status_code, 405)

    def testWithoutUser(self):
        """
        Call without login
        Should redirect to /
        """
        c = Client()
        response = c.post(self.url)
        self.assertRedirects(response, '/?next={0}'.format(self.url))

    def testEmptyArgs(self):
        """
        Call with empty args
        Should get a JSON which success is False
        """
        c = Client()
        result = c.login(username = 'alpha', password = 'alpha')
        self.assertTrue(result)
        response = c.post(self.url)
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.content.decode('utf-8'))
        self.assertFalse(result['success'])

    def testEmptyTitle(self):
        """
        Call with empty title
        Should get a JSON which success is False
        """
        c = Client()
        result = c.login(username = 'alpha', password = 'alpha')
        self.assertTrue(result)
        response = c.post(self.url, {
            'title': '',
        })
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.content.decode('utf-8'))
        self.assertFalse(result['success'])

    def testEmptyOthers(self):
        """
        Call with title but others are empty
        Should get a JSON which success is False
        """
        c = Client()
        result = c.login(username = 'alpha', password = 'alpha')
        self.assertTrue(result)
        response = c.post(self.url, {
            'title': '1',
        })
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.content.decode('utf-8'))
        self.assertFalse(result['success'])

    def testNonIntPhase(self):
        """
        Call with wrong phase
        Should get a JSON which success is False
        """
        c = Client()
        result = c.login(username = 'alpha', password = 'alpha')
        self.assertTrue(result)
        response = c.post(self.url, {
            'title': '1',
            'phase': 'a',
        })
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.content.decode('utf-8'))
        self.assertFalse(result['success'])

    def testNegativePhase(self):
        """
        Call with wrong phase
        Should get a JSON which success is False
        """
        c = Client()
        result = c.login(username = 'alpha', password = 'alpha')
        self.assertTrue(result)
        response = c.post(self.url, {
            'title': '1',
            'phase': '-1',
        })
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.content.decode('utf-8'))
        self.assertFalse(result['success'])

    def testGreaterThanFivePhase(self):
        """
        Call with wrong phase
        Should get a JSON which success is False
        """
        c = Client()
        result = c.login(username = 'alpha', password = 'alpha')
        self.assertTrue(result)
        response = c.post(self.url, {
            'title': '1',
            'phase': '6',
        })
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.content.decode('utf-8'))
        self.assertFalse(result['success'])

    def testWrongVolume(self):
        """
        Call with title and phase
        Should get a JSON which success is False
        """
        c = Client()
        result = c.login(username = 'alpha', password = 'alpha')
        self.assertTrue(result)
        response = c.post(self.url, {
            'title': '1',
            'phase': -1,
            'volume': 'a',
        })
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.content.decode('utf-8'))
        self.assertFalse(result['success'])

    def testAddOrder(self):
        """
        Call with title and phase
        Should get a JSON which success is True
        """
        c = Client()
        result = c.login(username = 'alpha', password = 'alpha')
        self.assertTrue(result)
        response = c.post(self.url, {
            'title': '1',
            'phase': -1,
            'volume': -1,
        })
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.content.decode('utf-8'))
        self.assertTrue(result['success'])
        result = Order.objects.get(user__exact=self.userAlpha, title__exact = '1')
        self.assertEqual(result.phase, -1)
        self.assertEqual(result.volume, -1)

    def testModifyTitle(self):
        """
        Call with new_title
        Should get a JSON wich success is False
        """
        c = Client()
        result = c.login(username = 'alpha', password = 'alpha')
        self.assertTrue(result)
        response = c.post(self.url, {
            'title': 'test_title',
            'new_title': 'new_test_title',
        })
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.content.decode('utf-8'))
        self.assertTrue(result['success'])
        result = Order.objects.filter(user__exact=self.userAlpha, title__exact = 'new_test_title')
        self.assertEqual(len(result), 1)

    def testModifyOrder(self):
        """
        Call with title and phase
        Should get a JSON which success is True
        """
        c = Client()
        result = c.login(username = 'alpha', password = 'alpha')
        self.assertTrue(result)
        response = c.post(self.url, {
            'title': 'test_title',
            'uri': 'new_test_uri',
        })
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.content.decode('utf-8'))
        self.assertTrue(result['success'])
        result = Order.objects.get(user__exact=self.userAlpha, title__exact = 'test_title')
        self.assertEqual(result.uri, 'new_test_uri')
        result = Order.objects.get(user__exact=self.userBeta, title__exact = 'test_title')
        self.assertEqual(result.uri, 'test_uri')

class DeleteTest(TestCase):

    @classmethod
    def setUpClass(cls):
        user = User.objects.create_user(username = 'alpha', password = 'alpha')
        o = Order(title = 'to-be-deleted', phase = -1, volume = -1, user=user)
        o.save()

    @classmethod
    def tearDownClass(cls):
        User.objects.all().delete()
        Order.objects.all().delete()

    def setUp(self):
        self.url = '/delete.cgi'

    def testGet(self):
        """
        Call with GET
        Should return failed request
        """
        c = Client()
        response = c.get(self.url)
        self.assertEqual(response.status_code, 405)

    def testWithoutUser(self):
        """
        Call without login
        Should redirect to /
        """
        c = Client()
        response = c.post(self.url)
        self.assertRedirects(response, '/?next={0}'.format(self.url))

    def testEmptyArgs(self):
        """
        Call with empty args
        Should return a JSON which success is False
        """
        c = Client()
        result = c.login(username = 'alpha', password = 'alpha')
        self.assertTrue(result)
        response = c.post(self.url)
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.content.decode('utf-8'))
        self.assertFalse(result['success'])

    def testEmptyTitle(self):
        """
        Call with empty title
        Should return a JSON which success is False
        """
        c = Client()
        result = c.login(username = 'alpha', password = 'alpha')
        self.assertTrue(result)
        response = c.post(self.url, {
            'title': '',
        })
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.content.decode('utf-8'))
        self.assertFalse(result['success'])

    def testDeleteNonExists(self):
        """
        Trying to delete non-exists record
        Should return a JSON which success is False
        """
        c = Client()
        result = c.login(username = 'alpha', password = 'alpha')
        self.assertTrue(result)
        response = c.post(self.url, {
        })
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.content.decode('utf-8'))
        self.assertFalse(result['success'])
        response = c.post(self.url, {
            'orders[]': 'non-exists',
        })
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.content.decode('utf-8'))
        self.assertFalse(result['success'])

    def testRightArgs(self):
        """
        Trying to delete non-exists record
        Should return a JSON which success is False
        """
        c = Client()
        result = c.login(username = 'alpha', password = 'alpha')
        self.assertTrue(result)
        response = c.post(self.url, {
            'orders[]': 'to-be-deleted',
        })
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.content.decode('utf-8'))
        self.assertTrue(result['success'])

class FetchTest(TestCase):

    def setUp(self):
        self.url = '/fetch.cgi'

    def testGet(self):
        c = Client()
        response = c.get(self.url)
        self.assertEqual(response.status_code, 405)

    def testWithoutUser(self):
        c = Client()
        response = c.post(self.url)
        self.assertRedirects(response, '/?next={0}'.format(self.url))
