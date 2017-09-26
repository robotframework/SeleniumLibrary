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


class ContextAware(object):

    def __init__(self, ctx):
        """Base class exposing attributes from the common context.

        :param SeleniumLibrary.SeleniumLibrary ctx:
            The library itself as a context object.
        """
        self.ctx = ctx

    @property
    def browser(self):
        return self.ctx.browser

    @property
    def browsers(self):
        return self.ctx._browsers

    @property
    def element_finder(self):
        return self.ctx.element_finder

    def find_element(self, locator, tag=None, first_only=True, required=True,
                     parent=None):
        return self.element_finder.find(locator, tag, first_only,
                                        required, parent)

    @property
    def table_element_finder(self):
        return self.ctx.table_element_finder
