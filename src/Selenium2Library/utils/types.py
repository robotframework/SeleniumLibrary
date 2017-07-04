# Originally based on  Robot Framework 3.0.2 robot.utils.robottypes
import sys


PY2 = sys.version_info[0] == 2


def is_string(item):
    if PY2:
        return isinstance(item, (str, unicode))
    return isinstance(item, str)


def is_truthy(item):
    if is_string(item):
        return item.upper() not in ('FALSE', 'NO', '', 'NONE')
    return bool(item)
