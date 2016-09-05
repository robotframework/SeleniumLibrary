from event import Event
from robot.libraries.BuiltIn import BuiltIn

class ScopeEvent(Event):
    def __init__(self, scope, action, *args, **kwargs):
        self.scope = scope
        self.action = action
        self.action_args = args
        self.action_kwargs = kwargs

        if scope == 'current':
            suite = BuiltIn().get_variable_value('${SUITE NAME}')
            test  = BuiltIn().get_variable_value('${TEST NAME}', '')
            self.scope = suite + '.' + test if test != '' else suite

    def trigger(self, *args, **kwargs):
        if args[0] == self.scope:
            self.action(*self.action_args, **self.action_kwargs)

class ScopeStart(ScopeEvent):
    name = 'scope_start'

class ScopeEnd(ScopeEvent):
    name = 'scope_end'
