# Copyright 2017- Robot Framework Foundation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Generic test library core for Robot Framework.

Main usage is easing creating larger test libraries. For more information and
examples see the project pages at
https://github.com/robotframework/PythonLibCore
"""

import inspect
import sys

try:
    from robot.api.deco import keyword
except ImportError:  # Support RF < 2.9
    def keyword(name=None, tags=()):
        if callable(name):
            return keyword()(name)

        def decorator(func):
            func.robot_name = name
            func.robot_tags = tags
            return func
        return decorator


PY2 = sys.version_info < (3,)

__version__ = '1.0.1.dev1'


class HybridCore(object):

    def __init__(self, library_components):
        self.keywords = {}
        self.attributes = {}
        self.add_library_components(library_components)
        self.add_library_components([self])

    def add_library_components(self, library_components):
        for component in library_components:
            for name, func in self._get_members(component):
                if callable(func) and hasattr(func, 'robot_name'):
                    kw = getattr(component, name)
                    kw_name = func.robot_name or name
                    self.keywords[kw_name] = kw
                    # Expose keywords as attributes both using original
                    # method names as well as possible custom names.
                    self.attributes[name] = self.attributes[kw_name] = kw

    def _get_members(self, component):
        if inspect.ismodule(component):
            return inspect.getmembers(component)
        if inspect.isclass(component):
            raise TypeError('Libraries must be modules or instances, got '
                            'class {!r} instead.'.format(component.__name__))
        if type(component) != component.__class__:
            raise TypeError('Libraries must be modules or new-style class '
                            'instances, got old-style class {!r} instead.'
                            .format(component.__class__.__name__))
        return self._get_members_from_instance(component)

    def _get_members_from_instance(self, instance):
        # Avoid calling properties by getting members from class, not instance.
        cls = type(instance)
        for name in dir(instance):
            owner = cls if hasattr(cls, name) else instance
            yield name, getattr(owner, name)

    def __getattr__(self, name):
        if name in self.attributes:
            return self.attributes[name]
        raise AttributeError('{!r} object has no attribute {!r}'
                             .format(type(self).__name__, name))

    def __dir__(self):
        if PY2:
            my_attrs = dir(type(self)) + list(self.__dict__)
        else:
            my_attrs = super().__dir__()
        return sorted(set(my_attrs) | set(self.attributes))

    def get_keyword_names(self):
        return sorted(self.keywords)


class DynamicCore(HybridCore):
    _get_keyword_tags_supported = False  # get_keyword_tags is new in RF 3.0.2

    def run_keyword(self, name, args, kwargs):
        return self.keywords[name](*args, **kwargs)

    def get_keyword_arguments(self, name):
        kw = self.keywords[name] if name != '__init__' else self.__init__
        args, defaults, varargs, kwargs = self._get_arg_spec(kw)
        args += ['{}={}'.format(name, value) for name, value in defaults]
        if varargs:
            args.append('*{}'.format(varargs))
        if kwargs:
            args.append('**{}'.format(kwargs))
        return args

    def _get_arg_spec(self, kw):
        if PY2:
            spec = inspect.getargspec(kw)
            keywords = spec.keywords
        else:
            spec = inspect.getfullargspec(kw)
            keywords = spec.varkw
        args = spec.args[1:] if inspect.ismethod(kw) else spec.args  # drop self
        defaults = spec.defaults or ()
        nargs = len(args) - len(defaults)
        mandatory = args[:nargs]
        defaults = zip(args[nargs:], defaults)
        return mandatory, defaults, spec.varargs, keywords

    def get_keyword_tags(self, name):
        self._get_keyword_tags_supported = True
        return self.keywords[name].robot_tags

    def get_keyword_documentation(self, name):
        if name == '__intro__':
            return inspect.getdoc(self) or ''
        if name == '__init__':
            return inspect.getdoc(self.__init__) or ''
        kw = self.keywords[name]
        doc = inspect.getdoc(kw) or ''
        if kw.robot_tags and not self._get_keyword_tags_supported:
            tags = 'Tags: {}'.format(', '.join(kw.robot_tags))
            doc = '{}\n\n{}'.format(doc, tags) if doc else tags
        return doc


class StaticCore(HybridCore):

    def __init__(self):
        HybridCore.__init__(self, [])
