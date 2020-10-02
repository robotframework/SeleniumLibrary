from datetime import datetime

import pytest
from mockito import mock, verify

from SeleniumLibrary.keywords import CookieKeywords
from SeleniumLibrary.keywords.cookie import CookieInformation


ALL_ARGS = {
    "name": "foo",
    "value": "123",
    "path": "/",
    "domain": "not.Here",
    "secure": True,
    "httpOnly": True,
    "expiry": 123,
}

pytestmark = pytest.mark.usefixtures('unstub')


@pytest.fixture()
def driver():
    return mock()


@pytest.fixture()
def ctx(driver):
    ctx = mock()
    ctx.driver = driver
    return ctx


@pytest.fixture()
def default_cookie():
    return {"name": "name", "value": "value"}


@pytest.fixture()
def cookie(ctx):
    return CookieKeywords(ctx)


def test_add_cookie_default(cookie, driver, default_cookie):
    cookie.add_cookie("name", "value")
    verify(driver).add_cookie(default_cookie)


def test_add_cookie_secure_true(cookie, default_cookie, driver):
    default_cookie["secure"] = True
    cookie.add_cookie("name", "value", path=None, domain=None, secure=True)
    verify(driver).add_cookie(default_cookie)

def test_add_cookie_secure_false(cookie, driver, default_cookie):
    cookie.add_cookie("name", "value", path=None, domain=None, secure=None)
    verify(driver).add_cookie(default_cookie)
    cookie.add_cookie("name", "value", path=None, domain=None, secure=False)
    default_cookie["secure"] = False
    verify(driver).add_cookie(default_cookie)
    cookie.add_cookie("name", "value", path=None, domain=None, secure=0)
    verify(driver, times=2).add_cookie(default_cookie)


def test_add_cookie_domain_true(cookie, default_cookie, driver):
    cookie.add_cookie("name", "value", path=None, domain="MyDomain", secure=None)
    cookie = default_cookie
    cookie["domain"] = "MyDomain"
    verify(driver).add_cookie(cookie)


def test_add_cookie_domain_false(cookie, driver, default_cookie):
    cookie.add_cookie("name", "value", path=None, domain=None, secure=None)
    verify(driver).add_cookie(default_cookie)


def test_add_cookie_path_true(cookie, default_cookie, driver):
    cookie.add_cookie("name", "value", path="/foo/bar", domain=None, secure=None)
    default_cookie["path"] = "/foo/bar"
    verify(driver).add_cookie(default_cookie)


def test_add_cookie_path_false(cookie, driver, default_cookie):
    cookie.add_cookie("name", "value", path=None, domain=None, secure=None)
    verify(driver).add_cookie(default_cookie)


def test_name_value_only():
    cookie = CookieInformation(name="foo", value="bar")
    assert cookie.name == "foo"
    assert cookie.value == "bar"


def test_all_args():
    cookie = CookieInformation(**ALL_ARGS)
    assert cookie.name == "foo"
    assert cookie.value == "123"
    assert cookie.path == "/"
    assert cookie.domain == "not.Here"
    assert cookie.secure is True
    assert cookie.httpOnly is True
    assert cookie.expiry == datetime.fromtimestamp(123)
    assert cookie.extra == {}


def test_extra_args():
    cookie_dict = ALL_ARGS.copy()
    cookie_dict["class_name"] = "seleniumLibary"
    cookie = CookieInformation(**cookie_dict)
    assert cookie.name == "foo"
    assert cookie.value == "123"
    assert cookie.extra == {"class_name": "seleniumLibary"}
    string = str(cookie)
    assert "\nextra={'class_name': 'seleniumLibary'}" in string


def test_no_mandatory_args():
    cookie_dict = ALL_ARGS.copy()
    del cookie_dict["name"]
    with pytest.raises(TypeError):
        CookieInformation(**cookie_dict)
