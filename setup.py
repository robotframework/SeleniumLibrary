#!/usr/bin/env python

from ez_setup import use_setuptools
use_setuptools()

from setuptools import setup, find_packages

VERSION = '0.5.3'

DESCRIPTION = """
Selenium2Library is a web testing library for Robot Framework
that leverages the Selenium 2 (WebDriver) libraries.
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
      install_requires = [
							'decorator >= 3.3.2',
							'selenium >= 2.8.1',
							'robotframework >= 2.6.3'
						 ],
      package_dir  = {'' : 'src'},
      packages     = find_packages('src', exclude=['ez_setup']),
      include_package_data = True,
      )
