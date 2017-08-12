# Originally based on  Robot Framework 3.0.2 robot.utils.robottypes
# Can be removed when library minimum required Robot Framework version is
# greater than 3.0.2. Then Robot Framework is_truthy should also support
# string NONE as Python False.
import sys


PY2 = sys.version_info[0] == 2

if PY2:
    def is_string(item):
        return isinstance(item, (str, unicode))
else:
    from robot.utils import is_string


def is_truthy(item):
    if is_string(item):
        return item.upper() not in ('FALSE', 'NO', '', 'NONE')
    return bool(item)


def is_falsy(item):
    return not is_truthy(item)
