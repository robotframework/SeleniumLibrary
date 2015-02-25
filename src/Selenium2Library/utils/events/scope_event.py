from event import Event

class ScopeEvent(Event):
    def __init__(self, scope, action, *args, **kwargs):
        self.scope = scope
        self.action = action
        self.action_args = args
        self.action_kwargs = kwargs

    def trigger(self, *args, **kwargs):
        if args[0] == self.scope:
            self.action(*self.action_args, **self.action_kwargs)

class ScopeStart(ScopeEvent):
    name = 'scope_start'

class ScopeEnd(ScopeEvent):
    name = 'scope_end'
