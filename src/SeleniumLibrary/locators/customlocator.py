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

from robot.libraries.BuiltIn import BuiltIn

from SeleniumLibrary.base import ContextAware


try:
    basestring
except NameError:
    basestring = str


class CustomLocator(ContextAware):

    def __init__(self, ctx, name, finder):
        ContextAware.__init__(self, ctx)
        self.name = name
        self.finder = finder

    def find(self, criteria, tag, constraints, parent):
        # Allow custom locators to be keywords or normal methods
        if isinstance(self.finder, basestring):
            element = BuiltIn().run_keyword(self.finder, parent,
                                            criteria, tag, constraints)
        elif hasattr(self.finder, '__call__'):
            element = self.finder(parent, criteria, tag, constraints)
        else:
            raise AttributeError('Invalid type provided for Custom Locator %s'
                                 % self.name)

        # Always return an array
        if hasattr(element, '__len__') and not isinstance(element, basestring):
            return element
        else:
            return [element]
