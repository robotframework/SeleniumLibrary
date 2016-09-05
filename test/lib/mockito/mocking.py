#!/usr/bin/env python
# coding: utf-8

import inspect
import invocation
from mock_registry import mock_registry
import warnings

__copyright__ = "Copyright 2008-2010, Mockito Contributors"
__license__ = "MIT"
__maintainer__ = "Mockito Maintainers"
__email__ = "mockito-python@googlegroups.com"

__all__ = ['mock', 'Mock']

class _Dummy(object): pass

class TestDouble(object): pass

class mock(TestDouble):
  def __init__(self, mocked_obj=None, strict=True):
    self.invocations = []
    self.stubbed_invocations = []
    self.original_methods = []
    self.stubbing = None
    self.verification = None
    if mocked_obj is None:
        mocked_obj = _Dummy()
        strict = False
    self.mocked_obj = mocked_obj
    self.strict = strict
    self.stubbing_real_object = False
    
    mock_registry.register(self)
  
  def __getattr__(self, method_name):
    if self.stubbing is not None:
      return invocation.StubbedInvocation(self, method_name)
    
    if self.verification is not None:
      return invocation.VerifiableInvocation(self, method_name)
      
    return invocation.RememberedInvocation(self, method_name)
  
  def remember(self, invocation):
    self.invocations.insert(0, invocation)
  
  def finish_stubbing(self, stubbed_invocation):
    self.stubbed_invocations.insert(0, stubbed_invocation)
    self.stubbing = None
    
  def expect_stubbing(self):
    self.stubbing = True
    
  def pull_verification(self):
    v = self.verification
    self.verification = None
    return v

  def has_method(self, method_name):
    return hasattr(self.mocked_obj, method_name)
    
  def get_method(self, method_name):
    return self.mocked_obj.__dict__.get(method_name)

  def set_method(self, method_name, new_method):
    setattr(self.mocked_obj, method_name, new_method)
    
  def replace_method(self, method_name, original_method):
    
    def new_mocked_method(*args, **kwargs): 
      # we throw away the first argument, if it's either self or cls  
      if inspect.isclass(self.mocked_obj) and not isinstance(original_method, staticmethod): 
          args = args[1:]
      call = self.__getattr__(method_name) # that is: invocation.RememberedInvocation(self, method_name)
      return call(*args, **kwargs)
      
    if isinstance(original_method, staticmethod):
      new_mocked_method = staticmethod(new_mocked_method)  
    elif isinstance(original_method, classmethod): 
      new_mocked_method = classmethod(new_mocked_method)  
    
    self.set_method(method_name, new_mocked_method)
    
  def stub(self, method_name):
    original_method = self.get_method(method_name)
    original = (method_name, original_method)
    self.original_methods.append(original)

    # If we're trying to stub real object(not a generated mock), then we should patch object to use our mock method.
    # TODO: Polymorphism was invented long time ago. Refactor this.
    if self.stubbing_real_object:
      self.replace_method(method_name, original_method)

  def unstub(self):  
    while self.original_methods:  
      method_name, original_method = self.original_methods.pop()      
      self.set_method(method_name, original_method)
       
def Mock(*args, **kwargs):
  '''A ``mock``() alias.
  
  Alias for compatibility. To be removed in version 1.0.
  '''
  warnings.warn("\n`Mock()` is deprecated, please use `mock()` (lower 'm') instead.", DeprecationWarning)
  return mock(*args, **kwargs)
