import unittest

from mockito import mock, unstub, verify

from SeleniumLibrary.keywords import CookieKeywords


class KeywordArgumentsCookieTest(unittest.TestCase):

    def setUp(self):
        self.ctx = mock()
        self.ctx.browser = self.browser = mock()
        self.cookie = CookieKeywords(self.ctx)
        self.default_cookie = {'name': 'name', 'value': 'value'}

    def tearDown(self):
        unstub()

    def test_add_cookie_default(self):
        self.cookie.add_cookie('name', 'value')
        verify(self.browser).add_cookie(self.default_cookie)

    def test_add_cookie_secure_true(self):
        cookie = self.default_cookie
        cookie['secure'] = True
        self.cookie.add_cookie('name', 'value', path='None', domain='None',
                               secure='True')
        verify(self.browser).add_cookie(cookie)
        self.cookie.add_cookie('name', 'value', path='None', domain='None',
                               secure='True_text')
        verify(self.browser, times=2).add_cookie(cookie)
        self.cookie.add_cookie('name', 'value', path='None', domain='None',
                               secure=True)
        verify(self.browser, times=3).add_cookie(cookie)
        self.cookie.add_cookie('name', 'value', path='None', domain='None',
                               secure='0')
        verify(self.browser, times=4).add_cookie(cookie)

    def test_add_cookie_secure_false(self):
        self.cookie.add_cookie('name', 'value', path='None', domain='None',
                               secure='None')
        verify(self.browser).add_cookie(self.default_cookie)
        self.cookie.add_cookie('name', 'value', path='None', domain='None',
                               secure='False')
        cookie = self.default_cookie
        cookie['secure'] = False
        verify(self.browser).add_cookie(cookie)
        self.cookie.add_cookie('name', 'value', path='None', domain='None',
                               secure=0)
        verify(self.browser, times=2).add_cookie(cookie)

    def test_add_cookie_domain_true(self):
        self.cookie.add_cookie('name', 'value', path='None', domain='MyDomain',
                               secure=None)
        cookie = self.default_cookie
        cookie['domain'] = 'MyDomain'
        verify(self.browser).add_cookie(cookie)

    def test_add_cookie_domain_false(self):
        self.cookie.add_cookie('name', 'value', path='None', domain='None',
                               secure=None)
        verify(self.browser).add_cookie(self.default_cookie)

    def test_add_cookie_path_true(self):
        self.cookie.add_cookie('name', 'value', path='/foo/bar', domain=None,
                               secure=None)
        cookie = self.default_cookie
        cookie['path'] = '/foo/bar'
        verify(self.browser).add_cookie(cookie)

    def test_add_cookie_path_false(self):
        self.cookie.add_cookie('name', 'value', path='None', domain=None,
                               secure=None)
        verify(self.browser).add_cookie(self.default_cookie)
