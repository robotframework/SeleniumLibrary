from __future__ import absolute_import
from builtins import str
from .browsercache import BrowserCache
from .librarylistener import LibraryListener
from . import events


def escape_xpath_value(value):
    value = str(value)
    if '"' in value and '\'' in value:
        parts_wo_apos = value.split('\'')
        return "concat('%s')" % "', \"'\", '".join(parts_wo_apos)
    if '\'' in value:
        return "\"%s\"" % value
    return "'%s'" % value