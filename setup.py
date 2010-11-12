#!/usr/bin/env python

#  Copyright 2008-2009 Nokia Siemens Networks Oyj
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

"""Setup script for Robot's SeleniumLibrary distributions"""

from distutils.core import setup

from os.path import abspath, dirname, join
execfile(join(dirname(abspath(__file__)), 'src', 'SeleniumLibrary', 'version.py'))


def main():
    setup(name         = 'robotframework-seleniumlibrary',
          version      = VERSION,
          description  = 'Web testing library for Robot Framework',
          author       = 'Robot Framework Developers',
          author_email = 'robotframework-users@googlegroups.com',
          url          = 'http://code.google.com/p/robotframework-seleniumlibrary',
          package_dir  = { '' : 'src'},
          packages     = ['SeleniumLibrary'],
          package_data = { 'SeleniumLibrary': ['lib/*.jar']} 
          )


if __name__ == "__main__":
    main()
