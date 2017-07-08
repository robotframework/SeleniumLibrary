# Originally based on  Robot Framework 3.0.2 robot.utils.robottypes
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
