import unittest

from mockito import mock, unstub, verify

from Selenium2Library.keywords import CookieKeywords


class KeywordArgumentsCookieTest(unittest.TestCase):

    def setUp(self):
        ctx = mock()
        ctx._browser = mock()
        self.cookie = CookieKeywords(ctx)
        self.ctx = ctx
        self.default_cookie = {'name': 'name', 'value': 'value'}

    def tearDown(self):
        unstub()

    def test_add_cookie_default(self):
        self.cookie.add_cookie('name', 'value')
        verify(self.ctx._browser).add_cookie(self.default_cookie)

    def test_add_cookie_secure_true(self):
        self.cookie.add_cookie('name', 'value', path='None', domain='None',
                               secure='True')
        cookie = self.default_cookie
        cookie['secure'] = True
        verify(self.ctx._browser).add_cookie(cookie)

    def test_add_cookie_secure_false(self):
        self.cookie.add_cookie('name', 'value', path='None', domain='None',
                               secure='None')
        verify(self.ctx._browser).add_cookie(self.default_cookie)

    def test_add_cookie_domain_true(self):
        self.cookie.add_cookie('name', 'value', path='None', domain='MyDomain',
                               secure=None)
        cookie = self.default_cookie
        cookie['domain'] = 'MyDomain'
        verify(self.ctx._browser).add_cookie(cookie)

    def test_add_cookie_domain_false(self):
        self.cookie.add_cookie('name', 'value', path='None', domain='False',
                               secure=None)
        verify(self.ctx._browser).add_cookie(self.default_cookie)

    def test_add_cookie_path_true(self):
        self.cookie.add_cookie('name', 'value', path='/foo/bar', domain=None,
                               secure=None)
        cookie = self.default_cookie
        cookie['path'] = '/foo/bar'
        verify(self.ctx._browser).add_cookie(cookie)

    def test_add_cookie_path_false(self):
        self.cookie.add_cookie('name', 'value', path='None', domain=None,
                               secure=None)
        verify(self.ctx._browser).add_cookie(self.default_cookie)
