#!/usr/bin/env python3
# coding: utf-8

from mockito import verify as verify_main

__author__ = "Serhiy Oplakanets <serhiy@oplakanets.com>"
__copyright__ = "Copyright 2008-2010, Mockito Contributors"
__license__ = "MIT"
__maintainer__ = "Mockito Maintainers"
__email__ = "mockito-python@googlegroups.com"

def verify(object, *args, **kwargs):
  kwargs['inorder'] = True
  return verify_main(object, *args, **kwargs)

