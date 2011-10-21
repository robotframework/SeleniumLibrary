#!/usr/bin/env python

import os, sys

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(THIS_DIR, "src", "Selenium2Library"))

from distutils.core import setup
import metadata

def main():
    if creating_source_distribution():
        run_doc_gen()
        run_demo_packaging()

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

def creating_source_distribution():
    return len(sys.argv) > 1 and sys.argv[1].lower() == 'sdist'

def run_doc_gen():
    sys.path.append(os.path.join(THIS_DIR, "doc"))
    import generate
    generate.main()

def run_demo_packaging():
    sys.path.append(os.path.join(THIS_DIR, "demo"))
    import package
    package.main()


if __name__ == '__main__':
    main()
