class MockRegistry:
  """Registers mock()s, ensures that we only have one mock() per mocked_obj, and
  iterates over them to unstub each stubbed method. """
  
  def __init__(self):
    self.mocks = {}
    
  def register(self, mock):
    self.mocks[mock.mocked_obj] = mock
        
  def mock_for(self, cls):
    return self.mocks.get(cls, None)
  
  def unstub_all(self):
    for mock in self.mocks.itervalues():    
      mock.unstub()
    self.mocks.clear()  

mock_registry = MockRegistry()