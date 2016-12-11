#!/usr/bin/env python

from os.path import abspath, dirname, join
from setuptools import setup


CURDIR = dirname(abspath(__file__))

execfile(join(CURDIR, 'src', 'Selenium2Library', 'version.py'))

DESCRIPTION = """
Selenium2Library is a web testing library for Robot Framework
that leverages the Selenium 2 (WebDriver) libraries.
"""[1:-1]

with open(join(CURDIR, 'requirements.txt')) as f:
    REQUIREMENTS = f.read().splitlines()

setup(name         = 'robotframework-selenium2library',
      version      = VERSION,
      description  = 'Web testing library for Robot Framework',
      long_description = DESCRIPTION,
      author       = 'Ryan Tomac , Ed Manlove , Jeremy Johnson',
      author_email = '<ryan@tomacfamily.com> ,  <devPyPlTw@verizon.net> ,  <jeremy@softworks.com.my>',
      url          = 'https://github.com/robotframework/Selenium2Library',
      license      = 'Apache License 2.0',
      keywords     = 'robotframework testing testautomation selenium selenium2 webdriver web',
      platforms    = 'any',
      classifiers  = [
                        "Development Status :: 5 - Production/Stable",
                        "License :: OSI Approved :: Apache Software License",
                        "Operating System :: OS Independent",
                        "Programming Language :: Python",
                        "Topic :: Software Development :: Testing"
                     ],
      install_requires = REQUIREMENTS,
      package_dir  = {'' : 'src'},
      packages     = ['Selenium2Library','Selenium2Library.keywords','Selenium2Library.locators',
                      'Selenium2Library.utils'],
      include_package_data = True,
      )
