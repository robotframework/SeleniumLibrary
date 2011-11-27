#!/usr/bin/env python

from setuptools import setup, find_packages

VERSION = '0.5.3'

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
      url          = 'https://github.com/rtomac/robotframework-selenium2library',
      license      = 'Apache License 2.0',
      keywords     = 'robotframework testing testautomation selenium selenium2 webdriver web',
      platforms    = 'any',
      classifiers  = [
                        "Development Status :: 4 - Beta",
                        #"Development Status :: 5 - Production/Stable",
                        "License :: OSI Approved :: Apache Software License",
                        "Operating System :: OS Independent",
                        "Programming Language :: Python",
                        "Topic :: Software Development :: Testing"
                     ],
      install_requires = ['decorator',
                          'selenium', ],
      package_dir  = {'' : 'src'},
      packages     = find_packages('src', exclude=['ez_setup']),
      include_package_data = True,
      )
