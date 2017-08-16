from robot.libraries.BuiltIn import BuiltIn

from Selenium2Library.base import LibraryComponent, keyword


class RunOnFailureKeywords(LibraryComponent):

    @keyword
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
        """
        old_keyword = self.ctx._run_on_failure_keyword
        old_keyword_text = old_keyword if old_keyword else "No keyword"

        new_keyword = keyword if keyword.strip().lower() != "nothing" else None
        new_keyword_text = new_keyword if new_keyword else "No keyword"

        self.ctx._run_on_failure_keyword = new_keyword
        self.info('%s will be run on failure.' % new_keyword_text)

        return old_keyword_text

    def run_on_failure(self):
        if not self.ctx._run_on_failure_keyword:
            return
        if self.ctx._running_on_failure_routine:
            return
        self.ctx._running_on_failure_routine = True
        try:
            BuiltIn().run_keyword(self.ctx._run_on_failure_keyword)
        except Exception as err:
            self.run_on_failure_error(err)
        finally:
            self.ctx._running_on_failure_routine = False

    def run_on_failure_error(self, err):
        err = ("Keyword '%s' could not be run on failure: %s"
               % (self.ctx._run_on_failure_keyword, err))
        if hasattr(self, 'warn'):
            self.warn(err)
            return
        raise Exception(err)
