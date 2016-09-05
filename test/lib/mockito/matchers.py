#!/usr/bin/env python
# coding: utf-8

'''Matchers for stubbing and verifications.

Common matchers for use in stubbing and verifications.
'''

__copyright__ = "Copyright 2008-2010, Mockito Contributors"
__license__ = "MIT"
__maintainer__ = "Mockito Maintainers"
__email__ = "mockito-python@googlegroups.com"

__all__ = ['any', 'contains', 'times']

class Matcher:
  def matches(self, arg):
    pass
  
class Any(Matcher):     
  def __init__(self, wanted_type=None):
    self.wanted_type = wanted_type
    
  def matches(self, arg):     
    if self.wanted_type:
      return isinstance(arg, self.wanted_type)
    else:
      return True
  
  def __repr__(self):
    return "<Any: %s>" % self.wanted_type  

class Contains(Matcher):
  def __init__(self, sub):
    self.sub = sub
      
  def matches(self, arg):
    if not hasattr(arg, 'find'):
      return  
    return self.sub and len(self.sub) > 0 and arg.find(self.sub) > -1

  def __repr__(self):
    return "<Contains: '%s'>" % self.sub  
  
      
def any(wanted_type=None):
  """Matches any() argument OR any(SomeClass) argument
     Examples:
       when(mock).foo(any()).thenReturn(1)
       verify(mock).foo(any(int))
  """
  return Any(wanted_type)     
        
def contains(sub):
  return Contains(sub)

def times(count):
  return count
