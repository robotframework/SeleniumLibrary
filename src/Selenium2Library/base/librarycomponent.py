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

from robot.api import logger

from .context import ContextAware


LOG_LEVELS = ['TRACE', 'DEBUG', 'INFO', 'WARN', 'ERROR']


class LibraryComponent(ContextAware):

    def __init__(self, ctx):
        ContextAware.__init__(self, ctx)

    @property
    def element_finder(self):
        return self.ctx.element_finder

    def info(self, msg, html=False):
        logger.info(msg, html)

    def debug(self, msg, html=False):
        logger.debug(msg, html)

    def log(self, msg, level='INFO', html=False):
        if level.upper() in LOG_LEVELS:
            logger.write(msg, level, html)

    def warn(self, msg, html=False):
        logger.warn(msg, html)

    def find_element(self, locator, tag=None, first_only=True, required=True):
        return self.element_finder.find(locator, tag, first_only, required)

    def assert_page_contains(self, locator, tag=None, message=None,
                             loglevel='INFO'):
        self.element_finder.assert_page_contains(locator, tag, message,
                                                 loglevel)

    def assert_page_not_contains(self, locator, tag=None, message=None,
                                 loglevel='INFO'):
        self.element_finder.assert_page_not_contains(locator, tag, message,
                                                     loglevel)
