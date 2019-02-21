from datetime import datetime
import unittest

from mockito import mock, unstub, verify

from SeleniumLibrary.keywords import CookieKeywords
from SeleniumLibrary.keywords.cookie import CookieInformation


class KeywordArgumentsCookieTest(unittest.TestCase):

    def setUp(self):
        self.ctx = mock()
        self.ctx.driver = self.driver = mock()
        self.cookie = CookieKeywords(self.ctx)
        self.default_cookie = {'name': 'name', 'value': 'value'}

    def tearDown(self):
        unstub()

    def test_add_cookie_default(self):
        self.cookie.add_cookie('name', 'value')
        verify(self.driver).add_cookie(self.default_cookie)

    def test_add_cookie_secure_true(self):
        cookie = self.default_cookie
        cookie['secure'] = True
        self.cookie.add_cookie('name', 'value', path='None', domain='None',
                               secure='True')
        verify(self.driver).add_cookie(cookie)
        self.cookie.add_cookie('name', 'value', path='None', domain='None',
                               secure='True_text')
        verify(self.driver, times=2).add_cookie(cookie)
        self.cookie.add_cookie('name', 'value', path='None', domain='None',
                               secure=True)
        verify(self.driver, times=3).add_cookie(cookie)
        self.cookie.add_cookie('name', 'value', path='None', domain='None',
                               secure='1')
        verify(self.driver, times=4).add_cookie(cookie)

    def test_add_cookie_secure_false(self):
        self.cookie.add_cookie('name', 'value', path='None', domain='None',
                               secure='None')
        verify(self.driver).add_cookie(self.default_cookie)
        self.cookie.add_cookie('name', 'value', path='None', domain='None',
                               secure='False')
        cookie = self.default_cookie
        cookie['secure'] = False
        verify(self.driver).add_cookie(cookie)
        self.cookie.add_cookie('name', 'value', path='None', domain='None',
                               secure=0)
        verify(self.driver, times=2).add_cookie(cookie)

    def test_add_cookie_domain_true(self):
        self.cookie.add_cookie('name', 'value', path='None', domain='MyDomain',
                               secure=None)
        cookie = self.default_cookie
        cookie['domain'] = 'MyDomain'
        verify(self.driver).add_cookie(cookie)

    def test_add_cookie_domain_false(self):
        self.cookie.add_cookie('name', 'value', path='None', domain='None',
                               secure=None)
        verify(self.driver).add_cookie(self.default_cookie)

    def test_add_cookie_path_true(self):
        self.cookie.add_cookie('name', 'value', path='/foo/bar', domain=None,
                               secure=None)
        cookie = self.default_cookie
        cookie['path'] = '/foo/bar'
        verify(self.driver).add_cookie(cookie)

    def test_add_cookie_path_false(self):
        self.cookie.add_cookie('name', 'value', path='None', domain=None,
                               secure=None)
        verify(self.driver).add_cookie(self.default_cookie)


class CookieObjecttest(unittest.TestCase):

    all_args = {'name': 'foo', 'value': '123', 'path': '/', 'domain': 'not.Here',
                'secure': True, 'httpOnly': True, 'expiry': 123}

    def test_name_value_only(self):
        cookie = CookieInformation(name='foo', value='bar')
        self.assertEqual(cookie.name, 'foo')
        self.assertEqual(cookie.value, 'bar')

    def test_all_args(self):
        cookie = CookieInformation(**self.all_args)
        self.assertEqual(cookie.name, 'foo')
        self.assertEqual(cookie.value, '123')
        self.assertEqual(cookie.path, '/')
        self.assertEqual(cookie.domain, 'not.Here')
        self.assertEqual(cookie.secure, True)
        self.assertEqual(cookie.httpOnly, True)
        self.assertEqual(cookie.expiry, datetime.fromtimestamp(123))
        self.assertEqual(cookie.extra, {})

    def test_extra_args(self):
        cookie_dict = self.all_args.copy()
        cookie_dict['class_name'] = 'seleniumLibary'
        cookie = CookieInformation(**cookie_dict)
        self.assertEqual(cookie.name, 'foo')
        self.assertEqual(cookie.value, '123')
        self.assertEqual(cookie.extra, {'class_name': 'seleniumLibary'})
        string = str(cookie)
        self.assertIn("\nextra={'class_name': 'seleniumLibary'}", string)

    def test_no_mandatory_args(self):
        cookie_dict = self.all_args.copy()
        del cookie_dict['name']
        with self.assertRaises(TypeError):
            CookieInformation(**cookie_dict)
