from . import events
from .browsercache import BrowserCache
from .librarylistener import LibraryListener


def escape_xpath_value(value):
    try:
        value = unicode(value)  # Python 2
    except NameError:
        pass                    # Python 3
    if '"' in value and '\'' in value:
        parts_wo_apos = value.split('\'')
        return "concat('%s')" % "', \"'\", '".join(parts_wo_apos)
    if '\'' in value:
        return "\"%s\"" % value
    return "'%s'" % value
