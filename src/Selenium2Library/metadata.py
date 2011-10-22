import os
import utils

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIRS = [ 'lib', 'resources' ]

VERSION = '0.5'
NAME = "robotframework-selenium2library"
PACKAGE_NAME = "Selenium2Library"

SHORT_DESCRIPTION = "Web testing library for Robot Framework"
LONG_DESCRIPTION = """
Selenium2Library is a web testing library for Robot Framework
that leverage the Selenium 2 (WebDriver) libraries.
"""[1:-1]

AUTHOR = "Robot Framework Developers"
AUTHOR_EMAIL = "robotframework@gmail.com"
PROJECT_URL = "https://github.com/rtomac/robotframework-selenium2library"

LICENSE = "Apache License 2.0"
KEYWORDS = "robotframework testing testautomation selenium selenium2 webdriver web"
PLATFORMS = "any"

TROVE_CLASSIFIERS = [
    "Development Status :: 4 - Beta",
    #"Development Status :: 5 - Production/Stable",
    "License :: OSI Approved :: Apache Software License",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Topic :: Software Development :: Testing"
]

def get_all_packages():
    packages = [ PACKAGE_NAME ]
    packages.extend(utils.get_child_packages_in(ROOT_DIR, exclusions=DATA_DIRS))
    return packages

def get_all_package_data():
    files = []
    for data_dir in DATA_DIRS:
        for path, dirnames, filenames in os.walk(os.path.join(ROOT_DIR, data_dir)):
            files.extend( [ os.path.join(path, filename)[len(ROOT_DIR)+1:]
                for filename in filenames ] )
    return { PACKAGE_NAME: files }
