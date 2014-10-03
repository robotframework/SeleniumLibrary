#!/usr/bin/env python

import sys
from os.path import join, dirname

from setuptools import setup

PY3 = sys.version_info[0] == 3

install_requires = [
    'decorator >= 3.3.2',
    'selenium >= 2.32.0',
    'docutils >= 0.8.1'
    ]

if PY3:
    install_requires.append('robotframework-python3 >= 2.6.0')
else:
    install_requires.append('robotframework >= 2.6.0')

exec(open(join(dirname(__file__), 'src', 'Selenium2Library', 'version.py')).read())

DESCRIPTION = """
Selenium2Library is a web testing library for Robot Framework
that leverages the Selenium 2 (WebDriver) libraries.
"""[1:-1]

setup(name         = 'robotframework-selenium2library',
      version      = VERSION,
      description  = 'Web testing library for Robot Framework',
      long_description = DESCRIPTION,
      author       = 'Ryan Tomac , Ed Manlove , Jeremy Johnson',
      author_email = '<ryan@tomacfamily.com> ,  <devPyPlTw@verizon.net> ,  <jeremy@softworks.com.my>',
      url          = 'https://github.com/rtomac/robotframework-selenium2library',
      license      = 'Apache License 2.0',
      keywords     = 'robotframework testing testautomation selenium selenium2 webdriver web',
      platforms    = 'any',
      classifiers  = [
                        "Development Status :: 5 - Production/Stable",
                        "License :: OSI Approved :: Apache Software License",
                        "Operating System :: OS Independent",
                        "Programming Language :: Python",
                        "Programming Language :: Python :: 2.7",
                        "Programming Language :: Python :: 3.4",
                        "Topic :: Software Development :: Testing"
                     ],
      install_requires = install_requires, 
      package_dir  = {'' : 'src'},
      packages     = ['Selenium2Library','Selenium2Library.keywords','Selenium2Library.locators',
                      'Selenium2Library.utils'],
      include_package_data = True,
      )
