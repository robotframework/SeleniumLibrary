from robot.libraries import BuiltIn
from keywordgroup import KeywordGroup

BUILTIN = BuiltIn.BuiltIn()

class _RunOnFailureKeywords(KeywordGroup):

    def __init__(self):
        self._run_on_failure_keyword = None
        self._running_on_failure_routine = False

    # Public

    def register_keyword_to_run_on_failure(self, keyword):
        """Sets the keyword to execute when a Selenium2Library keyword fails.

        `keyword_name` is the name of a keyword (from any available
        libraries) that  will be executed if a Selenium2Library keyword fails.
        It is not possible to use a keyword that requires arguments.
        Using the value "Nothing" will disable this feature altogether.

        The initial keyword to use is set in `importing`, and the
        keyword that is used by default is `Capture Page Screenshot`.
        Taking a screenshot when something failed is a very useful
        feature, but notice that it can slow down the execution.

        This keyword returns the name of the previously registered
        failure keyword. It can be used to restore the original
        value later.

        Example:
        | Register Keyword To Run On Failure  | Log Source | # Run `Log Source` on failure. |
        | ${previous kw}= | Register Keyword To Run On Failure  | Nothing    | # Disables run-on-failure functionality and stores the previous kw name in a variable. |
        | Register Keyword To Run On Failure  | ${previous kw} | # Restore to the previous keyword. |

        This run-on-failure functionality only works when running tests on Python/Jython 2.4
        or newer and it does not work on IronPython at all.
        """
        old_keyword = self._run_on_failure_keyword
        old_keyword_text = old_keyword if old_keyword is not None else "No keyword"

        new_keyword = keyword if keyword.strip().lower() != "nothing" else None
        new_keyword_text = new_keyword if new_keyword is not None else "No keyword"

        self._run_on_failure_keyword = new_keyword
        self._info('%s will be run on failure.' % new_keyword_text)

        return old_keyword_text
    
    # Private

    def _run_on_failure(self):
        if self._run_on_failure_keyword is None:
            return
        if self._running_on_failure_routine:
            return
        self._running_on_failure_routine = True
        try:
            BUILTIN.run_keyword(self._run_on_failure_keyword)
        except Exception, err:
            self._run_on_failure_error(err)
        finally:
            self._running_on_failure_routine = False

    def _run_on_failure_error(self, err):
        err = "Keyword '%s' could not be run on failure: %s" % (self._run_on_failure_keyword, err)
        if hasattr(self, '_warn'):
            self._warn(err)
            return
        raise Exception(err)
