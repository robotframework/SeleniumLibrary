from scope_event import ScopeStart, ScopeEnd

_registered_events = [ ScopeStart, ScopeEnd ]
_events = []

__all__ = [
    "on",
    "dispatch",
    "register_event"
]

def on(event_name, *args, **kwargs):
    for event in _registered_events:
        if event.name == event_name:
            _events.append(event(*args, **kwargs))
            return

def dispatch(event_name, *args, **kwargs):
    for event in _events:
        if event.name == event_name:
            event.trigger(*args, **kwargs)

def register_event(event):
    for registered_event in _registered_events:
        if event.name == registered_event.name:
            raise AttributeError("An event with the name " + event.name + " already exists.")
    _registered_events.append(event)
