import sys
import inspect
try:
    from decorator import decorator
except SyntaxError: # decorator module requires Python/Jython 2.4+
    decorator = None
if sys.platform == 'cli':
    decorator = None # decorator module doesn't work with IronPython 2.6

def _run_on_failure_decorator(method, *args, **kwargs):
    self = args[0]
    in_keyword = self._in_keyword
    self._in_keyword = True
    try:
        return method(*args, **kwargs)
    except Exception, err:
        if in_keyword and hasattr(self, '_run_on_failure') and not self._has_run_on_failure:
            self._has_run_on_failure = True
            self._run_on_failure()
        raise
    finally:
        if not in_keyword:
            self._in_keyword = False
            self._has_run_on_failure = False

class KeywordGroupMetaClass(type):
    def __new__(cls, clsname, bases, dict):
        if decorator:
            for name, method in dict.items():
                if not name.startswith('_') and inspect.isroutine(method):
                    dict[name] = decorator(_run_on_failure_decorator, method)
        return type.__new__(cls, clsname, bases, dict)

class KeywordGroup(object):
    __metaclass__ = KeywordGroupMetaClass
