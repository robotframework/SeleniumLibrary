#!/usr/bin/env python

from distutils.core import setup

from os.path import abspath, dirname, join
execfile(join(dirname(abspath(__file__)), 'src', 'SeleniumLibrary', 'version.py'))

DESCRIPTION = """
SeleniumLibrary is a web testing library for Robot Framework.
SeleniumLibrary leverages the popular Selenium web testing tool
and in addition also uses FlexPilot tool to provide Flex testing
capabilities.
"""[1:-1]
CLASSIFIERS = """
Development Status :: 5 - Production/Stable
License :: OSI Approved :: Apache Software License
Operating System :: OS Independent
Programming Language :: Python
Topic :: Software Development :: Testing
"""[1:-1]

setup(name         = 'robotframework-seleniumlibrary',
      version      = VERSION,
      description  = 'Web testing library for Robot Framework',
      long_description = DESCRIPTION,
      author       = 'Robot Framework Developers',
      author_email = 'robotframework@gmail.com',
      url          = 'http://code.google.com/p/robotframework-seleniumlibrary',
      license      = 'Apache License 2.0',
      keywords     = 'robotframework testing testautomation selenium web',
      platforms    = 'any',
      classifiers  = CLASSIFIERS.splitlines(),
      package_dir  = {'' : 'src'},
      packages     = ['SeleniumLibrary'],
      package_data = {'SeleniumLibrary': ['lib/*.jar',
                                          'lib/user-extensions.js',
                                          'firefoxprofile/*.*']},
      )
