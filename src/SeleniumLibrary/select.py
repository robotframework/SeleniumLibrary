#  Copyright 2008-2011 Nokia Siemens Networks Oyj
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from runonfailure import RunOnFailure


class Select(RunOnFailure):

    def get_list_items(self, locator):
        """Returns the values in the list identified by `locator`.

        List keywords work on both lists and combo boxes. Key attributes for
        lists are `id` and `name`. See `introduction` for details about
        locating elements.
        """
        return self._selenium.get_select_options(locator)

    def get_selected_list_value(self, locator):
        """Returns the value of the selected element from the list identified by `locator`.

        Return value is read from `value` attribute of the selected element.
        Fails if there are zero or more than one selection.

        List keywords work on both lists and combo boxes. Key attributes for
        lists are `id` and `name`. See `introduction` for details about
        locating elements.

        This keyword was added in SeleniumLibrary 2.8.
        """
        return self._selenium.get_selected_value(locator)

    def get_selected_list_values(self, locator):
        """Returns the values of selected elements (as a list) from the list identified by `locator`.

        Fails if there is no selection.

        List keywords work on both lists and combo boxes. Key attributes for
        lists are `id` and `name`. See `introduction` for details about
        locating elements.

        This keyword was added in SeleniumLibrary 2.8.
        """
        return self._selenium.get_selected_values(locator)

    def get_selected_list_label(self, locator):
        """Returns the visible label of the selected element from the list identified by `locator`.

        Fails if there are zero or more than one selection.

        List keywords work on both lists and combo boxes. Key attributes for
        lists are `id` and `name`. See `introduction` for details about
        locating elements.

        This keyword was added in SeleniumLibrary 2.8.
        """
        return self._selenium.get_selected_label(locator)

    def get_selected_list_labels(self, locator):
        """Returns the visible labels of selected elements (as a list) from the list identified by `locator`.

        Fails if there is no selection.

        List keywords work on both lists and combo boxes. Key attributes for
        lists are `id` and `name`. See `introduction` for details about
        locating elements.

        This keyword was added in SeleniumLibrary 2.8.
        """
        return self._selenium.get_selected_labels(locator)

    def list_selection_should_be(self, locator, *values):
        """Verifies the selection of list identified by `locator` is exactly `*values`.

        If you want to test that no option is selected, simply give no `values`.

        List keywords work on both lists and combo boxes. Key attributes for
        lists are `id` and `name`. See `introduction` for details about
        locating elements.
        """
        opts = values and 'options [ %s ]' % ' | '.join(values) or 'no options'
        self._info("Verifying list '%s' has %s selected." % (locator, opts))
        self.page_should_contain_list(locator)
        try:
            selected_values = self._selenium.get_selected_values(locator)
            selected_labels = self._selenium.get_selected_labels(locator)
        except Exception, err:
            if not values and self._error_contains(err, 'No option selected'):
                return
            raise
        err = "List '%s' should have had selection [ %s ] but it was [ %s ]" \
            % (locator, ' | '.join(values), ' | '.join(selected_labels))
        for expvalue in values:
            if expvalue not in selected_labels + selected_values:
                raise AssertionError(err)
        for label, value in zip(selected_labels, selected_values):
            if label not in values and value not in values:
                raise AssertionError(err)

    def select_from_list(self, locator, *values):
        """Selects `*values` from list identified by `locator`

        If more than one value is given for a single-selection list, the last
        value will be selected. If the target list is a multi-selection list,
        and `*values` is an empty list, all values of the list will be selected.

        List keywords work on both lists and combo boxes. Key attributes for
        lists are `id` and `name`. See `introduction` for details about
        locating elements.

        This keyword does not support waiting for possible page load
        automatically. If that is needed, keyword `Wait Until Page Loaded`
        can be used after this keyword.
        """
        selection = values and "values '%s'" % ', '.join(values) or 'all values'
        self._info("Selecting %s from list '%s'." % (selection, locator))
        values = list(values)
        if len(values) == 0:
            values = self._selenium.get_select_options(locator)
        if self._is_multiselect_list(locator):
            self._select_from_multiselect_list(locator, values)
        else:
            self._select_from_singleselect_list(locator, values)

    def _select_from_multiselect_list(self, locator, selection):
        self._call_method_for_list_elements('add_selection', locator, selection)

    def _select_from_singleselect_list(self, locator, selection):
        self._call_method_for_list_elements('select', locator, selection)

    def _is_multiselect_list(self, locator):
        try:
            self._selenium.get_attribute(locator+'@multiple')
            return True
        except Exception, err:
            if self._error_contains(err, 'attribute: %s@multiple' % locator):
                return False
            raise

    def _call_method_for_list_elements(self, method_name, locator, elements):
        method = getattr(self._selenium, method_name)
        for elem in elements:
            try:
                method(locator, elem)
            except:
                method(locator, 'value=%s' % elem)

    def unselect_from_list(self, locator, *values):
        """Unselects given values from list identified by locator.

        As a special case, giving empty list as `*selection` will remove all
        selections.

        List keywords work on both lists and combo boxes. Key attributes for
        lists are `id` and `name`. See `introduction` for details about
        locating elements.

        This keyword does not support waiting for possible page load
        automatically. If that is needed, keyword `Wait Until Page Loaded`
        can be used after this keyword.
        """
        selection = values and "values '%s'" % ', '.join(values) or 'all values'
        self._info("Unselecting %s from list '%s'." % (selection, locator))
        if not self._is_multiselect_list(locator):
            raise RuntimeError("Keyword 'Unselect from list' works only for "
                               "multiselect lists")
        if not values:
            self._selenium.remove_all_selections(locator)
        else:
            self._call_method_for_list_elements('remove_selection', locator,
                                                list(values))

    def select_all_from_list(self, locator, wait=''):
        """Selects all values from multi-select list identified by `id`.

        Key attributes for lists are `id` and `name`. See `introduction` for
        details about locating elements and about `wait` argument.
        """
        self._info("Selecting all values from list '%s'." % locator)
        selected_items = []
        if self._selenium.is_something_selected(locator):
            selected_items = self._selenium.get_selected_labels(locator)
        for item in self._selenium.get_select_options(locator):
            if item not in selected_items:
                self._add_to_selection(locator, item)
                if wait:
                    self.wait_until_page_loaded()

    def _add_to_selection(self, locator, item):
        try:
            self._selenium.add_selection(locator, item)
        except Exception, err:
            if self._error_contains(err, "Not a multi-select"):
                raise RuntimeError("Keyword 'Select all from list' works only "
                                   "for multiselect lists.")
            raise

    def list_should_have_no_selections(self, locator):
        """Verifies list identified by `locator` has no selections.

        List keywords work on both lists and combo boxes. Key attributes for
        lists are `id` and `name`. See `introduction` for details about
        locating elements.
        """
        self._info("Verifying list '%s' has no selection." % locator)
        if self._selenium.is_something_selected(locator):
            selection = ' | '.join(self._selenium.get_selected_labels(locator))
            raise AssertionError("List '%s' should have had no selection "
                                 "(selection was [ %s ])" % (locator, selection))

