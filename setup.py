#!/usr/bin/env python

from distutils.core import setup

from os.path import abspath, dirname, join
execfile(join(dirname(abspath(__file__)), 'src', 'Selenium2Library', 'version.py'))

DESCRIPTION = """
Selenium2Library is a web testing library for Robot Framework
that leverage the Selenium 2 (WebDriver) libraries.
"""[1:-1]

setup(name         = 'robotframework-selenium2library',
      version      = VERSION,
      description  = 'Web testing library for Robot Framework',
      long_description = DESCRIPTION,
      author       = 'Robot Framework Developers',
      author_email = 'robotframework@gmail.com',
      url          = 'http://code.google.com/p/robotframework-seleniumlibrary',
      license      = 'Apache License 2.0',
      keywords     = 'robotframework testing testautomation selenium web',
      platforms    = 'any',
      classifiers  = [
                        "Development Status :: 4 - Beta",
                        #"Development Status :: 5 - Production/Stable",
                        "License :: OSI Approved :: Apache Software License",
                        "Operating System :: OS Independent",
                        "Programming Language :: Python",
                        "Topic :: Software Development :: Testing"
                     ],
      package_dir  = {'' : 'src'},
      packages     = ['Selenium2Library'],
      package_data = {'Selenium2Library': ['resources/firefoxprofile/*.*']},
      )
