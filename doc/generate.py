#!/usr/bin/env python

from os.path import abspath, dirname, join
from libdoc import LibraryDoc, create_html_doc

docdir = dirname(abspath(__file__))
libpath = join(docdir, '..', 'src', 'Selenium2Library')
outpath = join(docdir, 'Selenium2Library.html')

lib = LibraryDoc(libpath)
create_html_doc(lib, outpath)
print lib.name, lib.version
print outpath
