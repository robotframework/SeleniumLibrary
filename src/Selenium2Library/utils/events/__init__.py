# Copyright 2008-2011 Nokia Networks
# Copyright 2011-2016 Ryan Tomac, Ed Manlove and contributors
# Copyright 2016-     Robot Framework Foundation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from .scope_event import ScopeStart, ScopeEnd


__all__ = [
    "on",
    "dispatch",
    "register_event"
]

_registered_events = [ScopeStart, ScopeEnd]
_events = []


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
