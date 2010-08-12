class Flex(object):

    def select_flex_application(self, locator, alias=None):
        self.page_should_contain_element(locator)
        self._wait_for_flex_ready(locator)
        return self._flex_apps.register(locator, alias)

    def _wait_for_flex_ready(self, locator, timeout=5000):
        # It seems that selenium timeout is always used so this timeout has no effect.
        self._selenium.do_command("waitForFlexReady", [locator, timeout])

    def click_flex_element(self, locator):
        self._flex_command('flexClick', 'name='+locator)

    def input_text_into_flex(self, locator, value):
        self._flex_command('flexType', 'name=%s,text=%s' % (locator, value))

    def text_in_flex_should_be(self, locator, expected):
        self._flex_command('flexAssertText', 'name=%s,validator=%s' %
                           (locator, expected.replace(',', '\\,')))

    def _flex_command(self, command, options):
        # TODO: Howto handle commas in option values??
        app = self._flex_apps.current
        if not app:
            raise RuntimeError('No Flex application selected.')
        self._selenium.do_command(command, [app, options])

