#!/usr/bin/env python

import os, sys

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(THIS_DIR, "src", "Selenium2Library"))

from distutils.core import setup
import metadata

def main():
    setup(
        name         = metadata.NAME,
        version      = metadata.VERSION,
        description  = metadata.SHORT_DESCRIPTION,
        long_description = metadata.LONG_DESCRIPTION,
        author       = metadata.AUTHOR,
        author_email = metadata.AUTHOR_EMAIL,
        url          = metadata.PROJECT_URL,
        license      = metadata.LICENSE,
        keywords     = metadata.KEYWORDS,
        platforms    = metadata.PLATFORMS,
        classifiers  = metadata.TROVE_CLASSIFIERS,
        package_dir  = {'' : 'src'},
        packages     = metadata.get_all_packages(),
        package_data = metadata.get_all_package_data(),
    )


if __name__ == '__main__':
    main()
