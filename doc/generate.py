#!/usr/bin/env python

import os, shutil
from libdoc import LibraryDoc, create_html_doc
from buildhtml import Builder

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.join(THIS_DIR, "..")
SRC_DIR = os.path.join(ROOT_DIR, "src")
LIB_DIR = os.path.join(SRC_DIR, "Selenium2Library")

def main():
    outpath = os.path.join(THIS_DIR, 'Selenium2Library.html')
    lib = LibraryDoc(LIB_DIR)
    create_html_doc(lib, outpath)
    print lib.name, lib.version
    print outpath


if __name__ == '__main__':
    main()
