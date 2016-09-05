#!/usr/bin/env python
# coding: utf-8

"""Mockito is a Test Spy framework."""
from __future__ import absolute_import
from .mockito import mock, verify, verifyNoMoreInteractions, \
    verifyZeroInteractions, when, unstub, ArgumentError
from . import inorder
from .spying import spy
from .verification import VerificationError

# Imports for compatibility
from .mocking import mock
from .matchers import any, contains, times  # use package import
# (``from mockito.matchers import any, contains``)
# instead of ``from mockito import any, contains``
from .verification import never

__copyright__ = "Copyright 2008-2010, Mockito Contributors"
__license__ = "MIT"
__maintainer__ = "Mockito Maintainers"
__email__ = "mockito-python@googlegroups.com"
__all__ = ['mock', 'spy', 'verify', 'verifyNoMoreInteractions',
           'verifyZeroInteractions', 'inorder', 'when', 'unstub',
           'VerificationError', 'ArgumentError',
           'Mock',  # deprecated
           'any',  # compatibility
           'contains',  # compatibility
           'never',  # compatibility
           'times'  # deprecated
           ]
