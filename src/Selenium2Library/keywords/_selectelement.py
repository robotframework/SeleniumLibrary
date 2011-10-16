from selenium.webdriver.remote.webelement import WebElement
from keywordgroup import KeywordGroup

class _SelectElementKeywords(KeywordGroup):

    # Public

    def get_list_items(self, locator):
        select, options = self._get_select_list_options(locator)
        return self._get_labels_for_options(options)

    def get_selected_list_label(self, locator):
        labels = self.get_selected_list_labels(locator)
        if len(labels) == 0: return None
        return labels[0]

    def get_selected_list_labels(self, locator):
        select, options = self._get_select_list_options_selected(locator)
        return self._get_labels_for_options(options)

    def get_selected_list_value(self, locator):
        values = self.get_selected_list_values(locator)
        if len(values) == 0: return None
        return values[0]

    def get_selected_list_values(self, locator):
        select, options = self._get_select_list_options_selected(locator)
        return self._get_values_for_options(options)

    def list_selection_should_be(self, locator, *items):
        items_str = items and "option(s) [ %s ]" % " | ".join(items) or "no options"
        self._info("Verifying list '%s' has %s selected." % (locator, items_str))
        items = list(items)
        self.page_should_contain_list(locator)
        select, options = self._get_select_list_options_selected(locator)
        if not items and len(options) == 0:
            return
        selected_values = self._get_values_for_options(options)
        selected_labels = self._get_labels_for_options(options)
        err = "List '%s' should have had selection [ %s ] but it was [ %s ]" \
            % (locator, ' | '.join(items), ' | '.join(selected_labels))
        for item in items:
            if item not in selected_values + selected_labels:
                raise AssertionError(err)
        for selected_value, selected_label in zip(selected_values, selected_labels):
            if selected_value not in items and selected_label not in items:
                raise AssertionError(err)

    def list_should_have_no_selections(self, locator):
        self._info("Verifying list '%s' has no selection." % locator)
        select, options = self._get_select_list_options_selected(locator)
        if options:
            selected_labels = self._get_labels_for_options(options)
            items_str = " | ".join(selected_labels)
            raise AssertionError("List '%s' should have had no selection "
                                 "(selection was [ %s ])" % (locator, items_str))

    def page_should_contain_list(self, locator, message='', loglevel='INFO'):
        self._page_should_contain_element(locator, 'list', message, loglevel)

    def page_should_not_contain_list(self, locator, message='', loglevel='INFO'):
        self._page_should_not_contain_element(locator, 'list', message, loglevel)

    def select_all_from_list(self, locator):
        self._info("Selecting all options from list '%s'." % locator)

        select = self._get_select_list(locator)
        if not self._is_multiselect_list(select):
            raise RuntimeError("Keyword 'Select all from list' works only for multiselect lists.")

        select, options = self._get_select_list_options(select)
        for i in range(len(options)):
            self._select_option_from_multi_select_list(select, options, i)

    def select_from_list(self, locator, *items):
        items_str = items and "option(s) '%s'" % ", ".join(items) or "all options"
        self._info("Selecting %s from list '%s'." % (items_str, locator))
        items = list(items)

        select, options = self._get_select_list_options(locator)
        is_multi_select = self._is_multiselect_list(select)
        select_func = self._select_option_from_multi_select_list if is_multi_select else self._select_option_from_single_select_list

        if not items:
            for i in range(len(options)):
                select_func(select, options, i)
            return

        option_values = self._get_values_for_options(options)
        option_labels = self._get_labels_for_options(options)
        for item in items:
            option_index = None
            try: option_index = option_values.index(item)
            except:
                try: option_index = option_labels.index(item)
                except: continue
            select_func(select, options, option_index)

    def unselect_from_list(self, locator, *items):
        items_str = items and "option(s) '%s'" % ", ".join(items) or "all options"
        self._info("Unselecting %s from list '%s'." % (items_str, locator))
        items = list(items)

        select = self._get_select_list(locator)
        if not self._is_multiselect_list(select):
            raise RuntimeError("Keyword 'Unselect from list' works only for multiselect lists.")

        if not items:
            self._unselect_all_options_from_multi_select_list(select)
            return

        select, options = self._get_select_list_options(select)
        option_values = self._get_values_for_options(options)
        option_labels = self._get_labels_for_options(options)
        for item in items:
            option_index = None
            try: option_index = option_values.index(item)
            except:
                try: option_index = option_labels.index(item)
                except: continue
            self._unselect_option_from_multi_select_list(select, options, option_index)

    # Private
    
    def _get_labels_for_options(self, options):
        labels = []
        for option in options:
            labels.append(option.text)
        return labels

    def _get_select_list(self, locator):
        return self._element_find(locator, True, True, 'select')

    def _get_select_list_options(self, select_list_or_locator):
        if isinstance(select_list_or_locator, WebElement):
            select = select_list_or_locator
        else:
            select = self._get_select_list(select_list_or_locator)
        return select, select.find_elements_by_tag_name('option')

    def _get_select_list_options_selected(self, select_list_or_locator):
        select, options = self._get_select_list_options(select_list_or_locator)
        selected = []
        for option in options:
            if option.is_selected():
                selected.append(option)
        return select, selected
    
    def _get_values_for_options(self, options):
        values = []
        for option in options:
             values.append(option.get_attribute('value'))
        return values

    def _is_multiselect_list(self, select):
        multiple_value = select.get_attribute('multiple')
        if multiple_value is not None and (multiple_value == 'true' or multiple_value == 'multiple'):
            return True
        return False

    def _select_option_from_multi_select_list(self, select, options, index):
        if not options[index].is_selected():
            options[index].click()

    def _select_option_from_single_select_list(self, select, options, index):
        select.click()
        options[index].click()

    def _unselect_all_options_from_multi_select_list(self, select):
        self._current_browser().execute_script("arguments[0].selectedIndex = -1;", select)

    def _unselect_option_from_multi_select_list(self, select, options, index):
        if options[index].is_selected():
            options[index].click()
