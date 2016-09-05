#!/usr/bin/env python
# coding: utf-8

'''Spying on real objects.'''

from invocation import RememberedProxyInvocation, VerifiableInvocation
from mocking import TestDouble

__author__ = "Serhiy Oplakanets <serhiy@oplakanets.com>"
__copyright__ = "Copyright 2009-2010, Mockito Contributors"
__license__ = "MIT"
__maintainer__ = "Mockito Maintainers"
__email__ = "mockito-python@googlegroups.com"

__all__ = ['spy']

def spy(original_object):
  return Spy(original_object)

class Spy(TestDouble):
  strict = True # spies always have to check if method exists
  
  def __init__(self, original_object):
    self.original_object = original_object
    self.invocations = []
    self.verification = None
    
  def __getattr__(self, name):        
    if self.verification:
      return VerifiableInvocation(self, name)
    else:
      return RememberedProxyInvocation(self, name)
  
  def remember(self, invocation):
    self.invocations.insert(0, invocation)
    
  def pull_verification(self):
    v = self.verification
    self.verification = None
    return v
    