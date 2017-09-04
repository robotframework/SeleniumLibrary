from collections import namedtuple

import selenium

SeleniumVersion = namedtuple('SeleniumVersion', 'major minor micro')
version = selenium.__version__.split('.')
selenium_version = SeleniumVersion(major=version[0], minor=version[1],
                                   micro=version[2])
