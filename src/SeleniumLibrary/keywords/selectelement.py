# Copyright 2008-2011 Nokia Networks
# Copyright 2011-2016 Ryan Tomac, Ed Manlove and contributors
# Copyright 2016-     Robot Framework Foundation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select

from SeleniumLibrary.base import LibraryComponent, keyword
from SeleniumLibrary.utils import is_truthy, plural_or_not as s


class SelectElementKeywords(LibraryComponent):

    @keyword
    def get_list_items(self, locator, values=False):
        """Returns all labels or values of selection list ``locator``.

        See the `Locating elements` section for details about the locator
        syntax.

        Returns visible labels by default, but values can be returned by
        setting the ``values`` argument to a true value (see `Boolean
        arguments`).

        Example:
        | ${labels} = | `Get List Items` | mylist              |             |
        | ${values} = | `Get List Items` | css:#example select | values=True |

        Support to return values is new in SeleniumLibrary 3.0.
        """
        options = self._get_options(locator)
        if is_truthy(values):
            return self._get_values(options)
        else:
            return self._get_labels(options)

    @keyword
    def get_selected_list_label(self, locator):
        """Returns label of selected option from selection list ``locator``.

        If there are multiple selected options, label of the first option
        is returned.

        See the `Locating elements` section for details about the locator
        syntax.
        """
        select = self._get_select_list(locator)
        return select.first_selected_option.text

    @keyword
    def get_selected_list_labels(self, locator):
        """Returns labels of selected options from selection list ``locator``.

        Starting from SeleniumLibrary 3.0, returns an empty list if there
        are no selections. In earlier versions this caused an error.

        See the `Locating elements` section for details about the locator
        syntax.
        """
        options = self._get_selected_options(locator)
        return self._get_labels(options)

    @keyword
    def get_selected_list_value(self, locator):
        """Returns value of selected option from selection list ``locator``.

        If there are multiple selected options, value of the first option
        is returned.

        See the `Locating elements` section for details about the locator
        syntax.
        """
        select = self._get_select_list(locator)
        return select.first_selected_option.get_attribute('value')

    @keyword
    def get_selected_list_values(self, locator):
        """Returns values of selected options from selection list ``locator``.

        Starting from SeleniumLibrary 3.0, returns an empty list if there
        are no selections. In earlier versions this caused an error.

        See the `Locating elements` section for details about the locator
        syntax.
        """
        options = self._get_selected_options(locator)
        return self._get_values(options)

    @keyword
    def list_selection_should_be(self, locator, *expected):
        """Verifies selection list ``locator`` has ``expected`` options selected.

        It is possible to give expected options both as visible labels and
        as values. Starting from SeleniumLibrary 3.0, mixing labels and
        values is not possible. Order of the selected options is not
        validated.

        If no expected options are given, validates that the list has
        no selections. A more explicit alternative is using `List Should
        Have No Selections`.

        See the `Locating elements` section for details about the locator
        syntax.

        Examples:
        | `List Selection Should Be` | gender    | Female          |        |
        | `List Selection Should Be` | interests | Test Automation | Python |
        """
        self.info("Verifying list '%s' has option%s [ %s ] selected."
                  % (locator, s(expected), ' | '.join(expected)))
        self.page_should_contain_list(locator)
        options = self._get_selected_options(locator)
        labels = self._get_labels(options)
        values = self._get_values(options)
        if sorted(expected) not in [sorted(labels), sorted(values)]:
            raise AssertionError("List '%s' should have had selection [ %s ] "
                                 "but selection was [ %s ]."
                                 % (locator, ' | '.join(expected),
                                    self._format_selection(labels, values)))

    def _format_selection(self, labels, values):
        return ' | '.join('%s (%s)' % (label, value)
                          for label, value in zip(labels, values))

    @keyword
    def list_should_have_no_selections(self, locator):
        """Verifies selection list ``locator`` has no options selected.

        See the `Locating elements` section for details about the locator
        syntax.
        """
        self.info("Verifying list '%s' has no selections." % locator)
        options = self._get_selected_options(locator)
        if options:
            selection = self._format_selection(self._get_labels(options),
                                               self._get_values(options))
            raise AssertionError("List '%s' should have had no selection "
                                 "but selection was [ %s ]."
                                 % (locator, selection))

    @keyword
    def page_should_contain_list(self, locator, message=None, loglevel='INFO'):
        """Verifies selection list ``locator`` is found from current page.

        See `Page Should Contain Element` for explanation about ``message``
        and ``loglevel`` arguments.

        See the `Locating elements` section for details about the locator
        syntax.
        """
        self.assert_page_contains(locator, 'list', message, loglevel)

    @keyword
    def page_should_not_contain_list(self, locator, message=None, loglevel='INFO'):
        """Verifies selection list ``locator`` is not found from current page.

        See `Page Should Contain Element` for explanation about ``message``
        and ``loglevel`` arguments.

        See the `Locating elements` section for details about the locator
        syntax.
        """
        self.assert_page_not_contains(locator, 'list', message, loglevel)

    @keyword
    def select_all_from_list(self, locator):
        """Selects all options from multi-selection list ``locator``.

        See the `Locating elements` section for details about the locator
        syntax.
        """
        self.info("Selecting all options from list '%s'." % locator)
        select = self._get_select_list(locator)
        if not select.is_multiple:
            raise RuntimeError("'Select All From List' works only with "
                               "multi-selection lists.")
        for i in range(len(select.options)):
            select.select_by_index(i)

    @keyword
    def select_from_list(self, locator, *options):
        """*DEPRECATED in SeleniumLibrary 3.2.* Use `Select From List By Label/Value/Index` instead.

        This keyword selects options based on labels or values, which makes
        it very complicated and slow. It has been deprecated in
        SeleniumLibrary 3.0, and dedicated keywords `Select From List By
        Label`, `Select From List By Value` and `Select From List By Index`
        should be used instead.
        """
        non_existing_items = []
        items_str = options and "option(s) '%s'" % ", ".join(options) or "all options"
        self.info("Selecting %s from list '%s'." % (items_str, locator))
        select = self._get_select_list(locator)
        if not options:
            for i in range(len(select.options)):
                select.select_by_index(i)
            return
        for item in options:
            try:
                select.select_by_value(item)
            except:
                try:
                    select.select_by_visible_text(item)
                except:
                    non_existing_items = non_existing_items + [item]
                    continue
        if any(non_existing_items):
            if select.is_multiple:
                raise ValueError("Options '%s' not in list '%s'." % (", ".join(non_existing_items), locator))
            else:
                if any (non_existing_items[:-1]):
                    items_str = non_existing_items[:-1] and "Option(s) '%s'" % ", ".join(non_existing_items[:-1])
                    self.warn("%s not found within list '%s'." % (items_str, locator))
                if options and options[-1] in non_existing_items:
                    raise ValueError("Option '%s' not in list '%s'." % (options[-1], locator))

    @keyword
    def select_from_list_by_index(self, locator, *indexes):
        """Selects options from selection list ``locator`` by ``indexes``.

        Indexes of list options start from 0.

        If more than one option is given for a single-selection list,
        the last value will be selected. With multi-selection lists all
        specified options are selected, but possible old selections are
        not cleared.

        See the `Locating elements` section for details about the locator
        syntax.
        """
        if not indexes:
            raise ValueError("No indexes given.")
        self.info("Selecting options from selection list '%s' by index%s %s."
                  % (locator, '' if len(indexes) == 1 else 'es',
                     ', '.join(indexes)))
        select = self._get_select_list(locator)
        for index in indexes:
            select.select_by_index(int(index))

    @keyword
    def select_from_list_by_value(self, locator, *values):
        """Selects options from selection list ``locator`` by ``values``.

        If more than one option is given for a single-selection list,
        the last value will be selected. With multi-selection lists all
        specified options are selected, but possible old selections are
        not cleared.

        See the `Locating elements` section for details about the locator
        syntax.
        """
        if not values:
            raise ValueError("No values given.")
        self.info("Selecting options from selection list '%s' by value%s %s."
                  % (locator, s(values), ', '.join(values)))
        select = self._get_select_list(locator)
        for value in values:
            select.select_by_value(value)

    @keyword
    def select_from_list_by_label(self, locator, *labels):
        """Selects options from selection list ``locator`` by ``labels``.

        If more than one option is given for a single-selection list,
        the last value will be selected. With multi-selection lists all
        specified options are selected, but possible old selections are
        not cleared.

        See the `Locating elements` section for details about the locator
        syntax.
        """
        if not labels:
            raise ValueError("No labels given.")
        self.info("Selecting options from selection list '%s' by label%s %s."
                  % (locator, s(labels), ', '.join(labels)))
        select = self._get_select_list(locator)
        for label in labels:
            select.select_by_visible_text(label)

    @keyword
    def unselect_all_from_list(self, locator):
        """Unselects all options from multi-selection list ``locator``.

        See the `Locating elements` section for details about the locator
        syntax.

        New in SeleniumLibrary 3.0.
        """
        self.info("Unselecting all options from list '%s'." % locator)
        select = self._get_select_list(locator)
        if not select.is_multiple:
            raise RuntimeError("Un-selecting options works only with "
                               "multi-selection lists.")
        select.deselect_all()

    @keyword
    def unselect_from_list(self, locator, *items):
        """*DEPRECATED in SeleniumLibrary 3.2.* Use `Unselect From List By Label/Value/Index` instead.

        This keyword unselects options based on labels or values, which makes
        it very complicated and slow. It has been deprecated in
        SeleniumLibrary 3.0, and dedicated keywords `Unselect From List By
        Label`, `Unselect From List By Value` and `Unselect From List By
        Index` should be used instead.
        """
        items_str = items and "option(s) '%s'" % ", ".join(items) or "all options"
        self.info("Unselecting %s from list '%s'." % (items_str, locator))
        select = self._get_select_list(locator)
        if not select.is_multiple:
            raise RuntimeError("Keyword 'Unselect from list' works only for multiselect lists.")
        if not items:
            select.deselect_all()
            return
        for item in items:
            # Only Selenium 2.52 and newer raise exceptions when there is no match.
            # For backwards compatibility reasons we want to ignore them.
            try:
                select.deselect_by_value(item)
            except NoSuchElementException:
                pass
            try:
                select.deselect_by_visible_text(item)
            except NoSuchElementException:
                pass

    @keyword
    def unselect_from_list_by_index(self, locator, *indexes):
        """Unselects options from selection list ``locator`` by ``indexes``.

        Indexes of list options start from 0. This keyword works only with
        multi-selection lists.

        See the `Locating elements` section for details about the locator
        syntax.
        """
        if not indexes:
            raise ValueError("No indexes given.")
        self.info("Un-selecting options from selection list '%s' by index%s "
                  "%s." % (locator, '' if len(indexes) == 1 else 'es',
                           ', '.join(indexes)))
        select = self._get_select_list(locator)
        if not select.is_multiple:
            raise RuntimeError("Un-selecting options works only with "
                               "multi-selection lists.")
        for index in indexes:
            select.deselect_by_index(int(index))

    @keyword
    def unselect_from_list_by_value(self, locator, *values):
        """Unselects options from selection list ``locator`` by ``values``.

        This keyword works only with multi-selection lists.

        See the `Locating elements` section for details about the locator
        syntax.
        """
        if not values:
            raise ValueError("No values given.")
        self.info("Un-selecting options from selection list '%s' by value%s "
                  "%s." % (locator, s(values), ', '.join(values)))
        select = self._get_select_list(locator)
        if not select.is_multiple:
            raise RuntimeError("Un-selecting options works only with "
                               "multi-selection lists.")
        for value in values:
            select.deselect_by_value(value)

    @keyword
    def unselect_from_list_by_label(self, locator, *labels):
        """Unselects options from selection list ``locator`` by ``labels``.

        This keyword works only with multi-selection lists.

        See the `Locating elements` section for details about the locator
        syntax.
        """
        if not labels:
            raise ValueError("No labels given.")
        self.info("Un-selecting options from selection list '%s' by label%s "
                  "%s." % (locator, s(labels), ', '.join(labels)))
        select = self._get_select_list(locator)
        if not select.is_multiple:
            raise RuntimeError("Un-selecting options works only with "
                               "multi-selection lists.")
        for label in labels:
            select.deselect_by_visible_text(label)

    def _get_select_list(self, locator):
        el = self.find_element(locator, tag='list')
        return Select(el)

    def _get_options(self, locator):
        return self._get_select_list(locator).options

    def _get_selected_options(self, locator):
        return self._get_select_list(locator).all_selected_options

    def _get_labels(self, options):
        return [opt.text for opt in options]

    def _get_values(self, options):
        return [opt.get_attribute('value') for opt in options]
