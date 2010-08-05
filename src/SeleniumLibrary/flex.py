class Flex(object):

    def select_flex_application(self, locator, alias=None):
        self.page_should_contain_element(locator)
        self.wait_for_flex_ready(locator)
        self._flex_apps.register(locator, alias)

    def flex_click(self, locator):
        self._selenium.do_command('flexClick', [self._flex_apps.current,
                                                'name=' + locator])

    def wait_for_flex_ready(self, locator, timeout=5000):
        # It seems that selenium timeout is always used so this timeout has no effect.
        self._selenium.do_command("waitForFlexReady", [locator, timeout])

    def flex_type(self, locator, value):
        self._selenium.do_command("flexType", [self._flex_apps.current,
                                               'name=%s,text=%s' % (locator, value)])

