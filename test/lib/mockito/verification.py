#!/usr/bin/env python
# coding: utf-8

__copyright__ = "Copyright 2008-2010, Mockito Contributors"
__license__ = "MIT"
__maintainer__ = "Mockito Maintainers"
__email__ = "mockito-python@googlegroups.com"

__all__ = ['never', 'VerificationError']

class VerificationError(AssertionError):
  '''Indicates error during verification of invocations.
  
  Raised if verification fails. Error message contains the cause.
  '''
  pass

class AtLeast(object):
  def __init__(self, wanted_count):
    self.wanted_count = wanted_count
    
  def verify(self, invocation, actual_count):
    if actual_count < self.wanted_count: 
      raise VerificationError("\nWanted at least: %i, actual times: %i" % (self.wanted_count, actual_count))
    
class AtMost(object):
  def __init__(self, wanted_count):
    self.wanted_count = wanted_count
    
  def verify(self, invocation, actual_count):
    if actual_count > self.wanted_count: 
      raise VerificationError("\nWanted at most: %i, actual times: %i" % (self.wanted_count, actual_count))

class Between(object):
  def __init__(self, wanted_from, wanted_to):
    self.wanted_from = wanted_from
    self.wanted_to = wanted_to
    
  def verify(self, invocation, actual_count):
    if actual_count < self.wanted_from or actual_count > self.wanted_to: 
      raise VerificationError("\nWanted between: [%i, %i], actual times: %i" % (self.wanted_from, self.wanted_to, actual_count))
    
class Times(object):
  def __init__(self, wanted_count):
    self.wanted_count = wanted_count
    
  def verify(self, invocation, actual_count):
    if actual_count == self.wanted_count:
        return  
    if actual_count == 0:
      raise VerificationError("\nWanted but not invoked: %s" % (invocation))
    else:
      if self.wanted_count == 0:
        raise VerificationError("\nUnwanted invocation of %s, times: %i" % (invocation, actual_count))
      else:
        raise VerificationError("\nWanted times: %i, actual times: %i" % (self.wanted_count, actual_count))
    
class InOrder(object):
  ''' 
  Verifies invocations in order.
  
  Verifies if invocation was in expected order, and if yes -- degrades to original Verifier (AtLeast, Times, Between, ...).
  '''
  
  def __init__(self, original_verification):
    '''    
    @param original_verification: Original verifiaction to degrade to if order of invocation was ok.
    '''
    self.original_verification = original_verification
    
  def verify(self, wanted_invocation, count):
    for invocation in reversed(wanted_invocation.mock.invocations):
      if not invocation.verified_inorder:
        if not wanted_invocation.matches(invocation):
          raise VerificationError("\nWanted %s to be invoked, got %s instead" % (wanted_invocation, invocation))
        invocation.verified_inorder = True
        break
    # proceed with original verification
    self.original_verification.verify(wanted_invocation, count)
    
never = 0
