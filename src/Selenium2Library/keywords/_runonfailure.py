from robot.libraries import BuiltIn
from keywordgroup import KeywordGroup

BUILTIN = BuiltIn.BuiltIn()

class _RunOnFailureKeywords(KeywordGroup):

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
            try:
                BUILTIN.run_keyword(self._run_on_failure_keyword)
            except Exception, err:
                raise Exception("Keyword '%s' could not be run on failure. %s" % 
                    (self._run_on_failure_keyword, err))
