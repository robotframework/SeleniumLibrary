from .browsercache import BrowserCache
from .librarylistener import LibraryListener
from .types import is_string, is_truthy, is_falsy


def escape_xpath_value(value):
    if '"' in value and '\'' in value:
        parts_wo_apos = value.split('\'')
        return "concat('%s')" % "', \"'\", '".join(parts_wo_apos)
    if '\'' in value:
        return "\"%s\"" % value
    return "'%s'" % value
