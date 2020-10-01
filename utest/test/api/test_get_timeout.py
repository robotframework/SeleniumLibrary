from datetime import timedelta

import pytest
from mockito import mock, unstub

from SeleniumLibrary.base import LibraryComponent


@pytest.fixture
def lib():
    ctx = mock()
    ctx.timeout = 5.0
    return LibraryComponent(ctx)


def teardown_function():
    unstub()


def test_timeout_as_none(lib: LibraryComponent):
    assert lib.get_timeout(None) == 5.0


def test_timeout_as_float(lib: LibraryComponent):
    assert lib.get_timeout(1.0) == 1.0


def test_timeout_as_timedelta(lib: LibraryComponent):
    assert lib.get_timeout(timedelta(seconds=0.1)) == 0.1
