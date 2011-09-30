#!/usr/bin/env python
# coding: utf-8

import verification
from mocking import mock, TestDouble
from mock_registry import mock_registry
from verification import VerificationError

__copyright__ = "Copyright 2008-2010, Mockito Contributors"
__license__ = "MIT"
__maintainer__ = "Mockito Maintainers"
__email__ = "mockito-python@googlegroups.com"

class ArgumentError(Exception):
  pass

def _multiple_arguments_in_use(*args):
  return len(filter(lambda x: x, args)) > 1    

def _invalid_argument(value):
  return (value is not None and value < 1) or value == 0

def _invalid_between(between):
  if between is not None:
    start, end = between
    if start > end or start < 0:
      return True
  return False

def verify(obj, times=1, atleast=None, atmost=None, between=None, inorder=False):
  if times < 0:
    raise ArgumentError("""'times' argument has invalid value. 
                           It should be at least 0. You wanted to set it to: %i""" % times)
  if _multiple_arguments_in_use(atleast, atmost, between):
    raise ArgumentError("""Sure you know what you are doing?
                           You can set only one of the arguments: 'atleast', 'atmost' or 'between'.""")
  if _invalid_argument(atleast):
    raise ArgumentError("""'atleast' argument has invalid value.
                           It should be at least 1.  You wanted to set it to: %i""" % atleast)
  if _invalid_argument(atmost):
    raise ArgumentError("""'atmost' argument has invalid value.
                           It should be at least 1.  You wanted to set it to: %i""" % atmost)
  if _invalid_between(between):
    raise ArgumentError("""'between' argument has invalid value.
                           It should consist of positive values with second number not greater than first
                           e.g. [1, 4] or [0, 3] or [2, 2]
                           You wanted to set it to: %s""" % between)

  if isinstance(obj, TestDouble):
    mocked_object = obj
  else:
    mocked_object = mock_registry.mock_for(obj)
               
  if atleast:
    mocked_object.verification = verification.AtLeast(atleast)
  elif atmost:
    mocked_object.verification = verification.AtMost(atmost)
  elif between:
    mocked_object.verification = verification.Between(*between)
  else:
    mocked_object.verification = verification.Times(times)
    
  if inorder:
    mocked_object.verification = verification.InOrder(mocked_object.verification)
    
  return mocked_object

def when(obj, strict=True):
  if isinstance(obj, mock):
    theMock = obj
  else:    
    theMock = mock_registry.mock_for(obj)
    if theMock is None:
      theMock = mock(obj, strict=strict)
      # If we call when on something that is not TestDouble that means we're trying to stub real object,
      # (class, module etc.). Not to be confused with generating stubs from real classes.
      theMock.stubbing_real_object = True

  theMock.expect_stubbing()
  return theMock

def unstub():
  """Unstubs all stubbed methods and functions"""
  mock_registry.unstub_all()

def verifyNoMoreInteractions(*mocks):
  for mock in mocks:
    for i in mock.invocations:
      if not i.verified:
        raise VerificationError("\nUnwanted interaction: " + str(i))
      
def verifyZeroInteractions(*mocks):
  verifyNoMoreInteractions(*mocks)
