import sys
import inspect
try:
    from decorator import decorator
except SyntaxError: # decorator module requires Python/Jython 2.4+
    decorator = None
if sys.platform == 'cli':
    decorator = None # decorator module doesn't work with IronPython 2.6
from robot.libraries import BuiltIn

BUILTIN = BuiltIn.BuiltIn()

def _run_keyword_on_failure_decorator(method, *args, **kwargs):
    try:
        return method(*args, **kwargs)
    except Exception, err:
        self = args[0]
        self._run_on_failure()
        raise

class _RunOnFailureType(type):
    def __new__(cls, clsname, bases, dict):
        if decorator:
            for name, method in dict.items():
                if not name.startswith('_') and inspect.isroutine(method):
                    dict[name] = decorator(_run_keyword_on_failure_decorator, method)
        return type.__new__(cls, clsname, bases, dict)

class _RunOnFailureKeywords(object):
    __metaclass__ = _RunOnFailureType

    def __init__(self):
        self._run_on_failure_keyword = None

    # Public

    def register_keyword_to_run_on_failure(self, keyword):
        old_keyword = self._run_on_failure_keyword
        old_keyword_text = old_keyword if old_keyword is not None else "No keyword"

        new_keyword = keyword if keyword.strip().lower() != "nothing" else None
        new_keyword_text = new_keyword if new_keyword is not None else "No keyword"

        self._run_on_failure_keyword = new_keyword
        self._info('%s will be run on failure.' % new_keyword_text)

        return old_keyword_text
    
    # Private

    def _run_on_failure(self):
        if self._run_on_failure_keyword is not None:
            BUILTIN.run_keyword(self._run_on_failure_keyword)
