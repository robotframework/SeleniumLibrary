#!/usr/bin/env python

import os, shutil
from libdoc import LibraryDoc, create_html_doc
from buildhtml import Builder

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.join(THIS_DIR, "..")
SRC_DIR = os.path.join(ROOT_DIR, "src")
LIB_DIR = os.path.join(SRC_DIR, "Selenium2Library")

README_FILES = [
    "README.txt",
    "INSTALL.txt",
    "test/README.txt"
]

def main():
    build_lib_docs()
    build_readmes()

def build_lib_docs():
    outpath = os.path.join(THIS_DIR, 'Selenium2Library.html')
    lib = LibraryDoc(LIB_DIR)
    create_html_doc(lib, outpath)
    print lib.name, lib.version
    print outpath

def build_readmes():
    try:
        import docutils
    except:
        print "Readme files will not be built into HTML, docutils not installed"
        return
    for readme_relative_path in README_FILES:
        readme_abs_path = os.path.join(ROOT_DIR, readme_relative_path.replace('/', os.sep))
        readme_path_parts = os.path.split(readme_abs_path)
        Builder().process_txt(readme_path_parts[0], readme_path_parts[1])
        readme_html_path = os.path.splitext(readme_abs_path)[0] + '.html'
        target_html_name = os.path.splitext(readme_relative_path.replace('/', '-'))[0] + '.html'
        target_html_path = os.path.join(THIS_DIR, target_html_name)
        if os.path.exists(target_html_path):
            os.remove(target_html_path)
        os.rename(readme_html_path, target_html_path)
        print "    ::: Saved: %s" % target_html_name


if __name__ == '__main__':
    main()
