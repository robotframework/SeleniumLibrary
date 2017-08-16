from robot.api import logger
from robot.utils import NormalizedDict
from selenium.webdriver.remote.webelement import WebElement

from .customlocator import CustomLocator
from Selenium2Library.base import ContextAware
from Selenium2Library.utils import escape_xpath_value, events
from Selenium2Library.utils import is_falsy


class ElementFinder(ContextAware):

    def __init__(self, ctx):
        ContextAware.__init__(self, ctx)
        strategies = {
            'identifier': self._find_by_identifier,
            'id': self._find_by_id,
            'name': self._find_by_name,
            'xpath': self._find_by_xpath,
            'dom': self._find_by_dom,
            'link': self._find_by_link_text,
            'partial link': self._find_by_partial_link_text,
            'css': self._find_by_css_selector,
            'class': self._find_by_class_name,
            'jquery': self._find_by_sizzle_selector,
            'sizzle': self._find_by_sizzle_selector,
            'tag': self._find_by_tag_name,
            'scLocator': self._find_by_sc_locator,
            'default': self._find_by_default
        }
        self._strategies = NormalizedDict(initial=strategies, caseless=True,
                                          spaceless=True)
        self._default_strategies = list(strategies)
        self._key_attrs = {
            None: ['@id', '@name'],
            'a': ['@id', '@name', '@href',
                  'normalize-space(descendant-or-self::text())'],
            'img': ['@id', '@name', '@src', '@alt'],
            'input': ['@id', '@name', '@value', '@src'],
            'button': ['@id', '@name', '@value',
                       'normalize-space(descendant-or-self::text())']
        }

    def find(self, locator, tag=None, first_only=True, required=True):
        if isinstance(locator, WebElement):
            return locator
        prefix, criteria = self._parse_locator(locator)
        if prefix not in self._strategies:
            raise ValueError("Element locator with prefix '%s' "
                             "is not supported." % prefix)
        strategy = self._strategies.get(prefix)
        tag, constraints = self._get_tag_and_constraints(tag)
        elements = strategy(criteria, tag, constraints)
        if required and not elements:
            raise ValueError("Element locator '{}' did not match any "
                             "elements.".format(locator))
        if first_only:
            if not elements:
                return None
            return elements[0]
        return elements

    def assert_page_contains(self, locator, tag=None, message=None,
                             loglevel='INFO'):
        element_name = tag if tag else 'element'
        if not self.find(locator, tag, required=False):
            if is_falsy(message):
                message = ("Page should have contained %s '%s' but did not"
                           % (element_name, locator))
            self.ctx.log_source(loglevel)  # TODO: Could this moved to base
            raise AssertionError(message)
        logger.info("Current page contains %s '%s'." % (element_name, locator))

    def assert_page_not_contains(self, locator, tag=None, message=None,
                                 loglevel='INFO'):
        element_name = tag if tag else 'element'
        if self.find(locator, tag, required=False):
            if is_falsy(message):
                message = ("Page should not have contained %s '%s'"
                           % (element_name, locator))
            self.ctx.log_source(loglevel)  # TODO: Could this moved to base
            raise AssertionError(message)
        logger.info("Current page does not contain %s '%s'."
                    % (element_name, locator))

    def get_value(self, locator, tag=None):
        element = self.find(locator, tag, required=False)
        return element.get_attribute('value') if element else None

    def register(self, strategy_name, strategy_keyword, persist=False):
        strategy = CustomLocator(self.ctx, strategy_name, strategy_keyword)
        if strategy.name in self._strategies:
            raise RuntimeError("The custom locator '%s' cannot be registered. "
                               "A locator of that name already exists."
                               % strategy.name)
        self._strategies[strategy.name] = strategy.find
        if is_falsy(persist):
            # Unregister after current scope ends
            events.on('scope_end', 'current', self.unregister, strategy.name)

    def unregister(self, strategy_name):
        if strategy_name in self._default_strategies:
            raise RuntimeError("Cannot unregister the default strategy '%s'."
                               % strategy_name)
        elif strategy_name not in self._strategies:
            logger.info("Cannot unregister the non-registered strategy '%s'."
                        % strategy_name)
        else:
            del self._strategies[strategy_name]

    def has_strategy(self, strategy_name):
        return strategy_name in self.strategies

    def _find_by_identifier(self, criteria, tag, constraints):
        elements = self._normalize_result(
            self.browser.find_elements_by_id(criteria))
        elements.extend(self._normalize_result(
            self.browser.find_elements_by_name(criteria)))
        return self._filter_elements(elements, tag, constraints)

    def _find_by_id(self, criteria, tag, constraints):
        return self._filter_elements(
            self.browser.find_elements_by_id(criteria),
            tag, constraints)

    def _find_by_name(self, criteria, tag, constraints):
        return self._filter_elements(
            self.browser.find_elements_by_name(criteria),
            tag, constraints)

    def _find_by_xpath(self, criteria, tag, constraints):
        return self._filter_elements(
            self.browser.find_elements_by_xpath(criteria),
            tag, constraints)

    def _find_by_dom(self, criteria, tag, constraints):
        result = self.browser.execute_script("return %s;" % criteria)
        if result is None:
            return []
        if not isinstance(result, list):
            result = [result]
        return self._filter_elements(result, tag, constraints)

    def _find_by_sizzle_selector(self, criteria, tag, constraints):
        js = "return jQuery('%s').get();" % criteria.replace("'", "\\'")
        return self._filter_elements(
            self.browser.execute_script(js),
            tag, constraints)

    def _find_by_link_text(self, criteria, tag, constraints):
        return self._filter_elements(
            self.browser.find_elements_by_link_text(criteria),
            tag, constraints)

    def _find_by_partial_link_text(self, criteria, tag, constraints):
        return self._filter_elements(
            self.browser.find_elements_by_partial_link_text(criteria),
            tag, constraints)

    def _find_by_css_selector(self, criteria, tag, constraints):
        return self._filter_elements(
            self.browser.find_elements_by_css_selector(criteria),
            tag, constraints)

    def _find_by_class_name(self, criteria, tag, constraints):
        return self._filter_elements(
            self.browser.find_elements_by_class_name(criteria),
            tag, constraints)

    def _find_by_tag_name(self, criteria, tag, constraints):
        return self._filter_elements(
            self.browser.find_elements_by_tag_name(criteria),
            tag, constraints)

    def _find_by_sc_locator(self, criteria, tag, constraints):
        js = "return isc.AutoTest.getElement('%s')" % criteria.replace("'", "\\'")
        return self._filter_elements([self.browser.execute_script(js)],
                                     tag, constraints)

    def _find_by_default(self, criteria, tag, constraints):
        if tag in self._key_attrs:
            key_attrs = self._key_attrs[tag]
        else:
            key_attrs = self._key_attrs[None]
        xpath_criteria = escape_xpath_value(criteria)
        xpath_tag = tag if tag is not None else '*'
        xpath_constraints = self._get_xpath_constraints(constraints)
        xpath_searchers = ["%s=%s" % (attr, xpath_criteria) for attr in key_attrs]
        xpath_searchers.extend(self._get_attrs_with_url(key_attrs, criteria))
        xpath = "//%s[%s%s(%s)]" % (
            xpath_tag,
            ' and '.join(xpath_constraints),
            ' and ' if xpath_constraints else '',
            ' or '.join(xpath_searchers)
        )
        return self._normalize_result(
            self.browser.find_elements_by_xpath(xpath))

    def _get_xpath_constraints(self, constraints):
        xpath_constraints = [self._get_xpath_constraint(name, value)
                             for name, value in constraints.items()]
        return xpath_constraints

    def _get_xpath_constraint(self, name, value):
        if isinstance(value, list):
            return "@%s[. = '%s']" % (name, "' or . = '".join(value))
        else:
            return "@%s='%s'" % (name, value)

    def _get_tag_and_constraints(self, tag):
        if tag is None:
            return None, {}
        tag = tag.lower()
        constraints = {}
        if tag == 'link':
            tag = 'a'
        if tag == 'partial link':
            tag = 'a'
        elif tag == 'image':
            tag = 'img'
        elif tag == 'list':
            tag = 'select'
        elif tag == 'radio button':
            tag = 'input'
            constraints['type'] = 'radio'
        elif tag == 'checkbox':
            tag = 'input'
            constraints['type'] = 'checkbox'
        elif tag == 'text field':
            tag = 'input'
            constraints['type'] = ['date', 'datetime-local', 'email', 'month',
                                   'number', 'password', 'search', 'tel',
                                   'text', 'time', 'url', 'week']
        elif tag == 'file upload':
            tag = 'input'
            constraints['type'] = 'file'
        elif tag == 'text area':
            tag = 'textarea'
        return tag, constraints

    def _parse_locator(self, locator):
        if locator.startswith(('//', '(//')):
            return 'xpath', locator
        if '=' not in locator:
            return 'default', locator
        prefix, criteria = locator.split('=', 1)
        return prefix.strip(), criteria.lstrip()

    def _element_matches(self, element, tag, constraints):
        if not element.tag_name.lower() == tag:
            return False
        for name in constraints:
            if isinstance(constraints[name], list):
                if element.get_attribute(name) not in constraints[name]:
                    return False
            elif element.get_attribute(name) != constraints[name]:
                return False
        return True

    def _filter_elements(self, elements, tag, constraints):
        elements = self._normalize_result(elements)
        if tag is None:
            return elements
        return [element for element in elements if self._element_matches(element, tag, constraints)]

    def _get_attrs_with_url(self, key_attrs, criteria):
        attrs = []
        url = None
        xpath_url = None
        for attr in ['@src', '@href']:
            if attr in key_attrs:
                if url is None or xpath_url is None:
                    url = self._get_base_url() + "/" + criteria
                    xpath_url = escape_xpath_value(url)
                attrs.append("%s=%s" % (attr, xpath_url))
        return attrs

    def _get_base_url(self):
        url = self.browser.current_url
        if '/' in url:
            url = '/'.join(url.split('/')[:-1])
        return url

    def _normalize_result(self, elements):
        if not isinstance(elements, list):
            logger.debug("WebDriver find returned %s" % elements)
            return []
        return elements
