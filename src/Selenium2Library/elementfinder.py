from robot import utils
from types import *

class ElementFinder(object):

    def __init__(self):
        self._strategies = {
            'identifier': self._find_by_identifier,
            'id': self._find_by_id,
            'name': self._find_by_name,
            'xpath': self._find_by_xpath,
            'link': self._find_by_link_text,
            'css': self._find_by_css_selector,
            'tag': self._find_by_tag_name,
            None: self._find_by_default
        }

    def find(self, browser, locator, tag=None):
        (prefix, criteria) = self._parse_locator(locator)
        if tag is not None:
            tag = self._tag_synonyms.get(tag, tag)
        strategy = self._strategies.get(prefix)
        if strategy is None:
            raise ValueError("Locator with prefix '" + prefix + "' is not supported")
        return strategy(browser, criteria, tag)

    # Strategy routines, private

    def _find_by_identifier(self, browser, criteria, tag):
        elements = browser.find_elements_by_id(criteria)
        elements.extend(browser.find_elements_by_name(criteria))
        return self._filter_by_tag(elements, tag)

    def _find_by_id(self, browser, criteria, tag):
        return self._filter_by_tag(
            browser.find_elements_by_id(criteria),
            tag)

    def _find_by_name(self, browser, criteria, tag):
        return self._filter_by_tag(
            browser.find_elements_by_name(criteria),
            tag)

    def _find_by_xpath(self, browser, criteria, tag):
        return self._filter_by_tag(
            browser.find_elements_by_xpath(criteria),
            tag)

    def _find_by_link_text(self, browser, criteria, tag):
        return self._filter_by_tag(
            browser.find_elements_by_link_text(criteria),
            tag)

    def _find_by_css_selector(self, browser, criteria, tag):
        return self._filter_by_tag(
            browser.find_elements_by_css_selector(criteria),
            tag)

    def _find_by_tag_name(self, browser, criteria, tag):
        return self._filter_by_tag(
            browser.find_elements_by_tag_name(criteria),
            tag)

    def _find_by_default(self, browser, criteria, tag):
        if criteria.startswith('//'):
            return self._find_by_xpath(browser, criteria, tag)
        return self._find_by_key_attrs(browser, criteria, tag)

    def _find_by_key_attrs(self, browser, criteria, tag):
        key_attrs = self._key_attrs.get(None)
        if tag is not None:
            key_attrs = self._key_attrs.get(tag, key_attrs)

        xpath_criteria = self._xpath_criteria_escape(criteria)
        xpath_tag = tag if tag is not None else '*'
        xpath_attrs = ["%s=%s" % (attr, xpath_criteria) for attr in key_attrs]
        xpath_attrs.extend(
            self._get_attrs_with_url(key_attrs, criteria, browser))
        xpath = "//%s[%s]" % (xpath_tag, ' or '.join(xpath_attrs))

        return browser.find_elements_by_xpath(xpath)

    # Private

    _tag_synonyms = {
        'link': 'a',
        'image': 'img',
        'radio button': 'input'
    }
    _key_attrs = {
        None: ['@id', '@name'],
        'a': ['@id', '@name', '@href', 'normalize-space(descendant-or-self::text())'],
        'img': ['@id', '@name', '@src', '@alt'],
        'input': ['@id', '@name', '@value', '@src'],
        'button': ['@id', '@name', '@value', 'normalize-space(descendant-or-self::text())']
    }

    def _filter_by_tag(self, elements, tag):
        if tag is None: return elements
        return filter(
            lambda element: element.tag_name.lower() == tag,
            elements)

    def _get_attrs_with_url(self, key_attrs, criteria, browser):
        attrs = []
        url = None
        xpath_url = None
        for attr in ['@src', '@href']:
            if attr in key_attrs:
                if url is None or xpath_url is None:
                    url = self._get_base_url(browser) + "/" + criteria
                    xpath_url = self._xpath_criteria_escape(url)
                attrs.append("%s=%s" % (attr, xpath_url))
        return attrs

    def _get_base_url(self, browser):
        url = browser.get_current_url()
        if '/' in url:
            url = '/'.join(url.split('/')[:-1])
        return url

    def _parse_locator(self, locator):
        prefix = None
        criteria = locator
        if not locator.startswith('//'):
            locator_parts = locator.partition('=')
            if len(locator_parts[1]) > 0:
                prefix = locator_parts[0].lower()
                criteria = locator_parts[2]
        return (prefix, criteria)

    def _xpath_criteria_escape(self, str):
        if '"' in str and '\'' in str:
            parts_wo_apos = str.split('\'')
            return "concat('%s')" % "', \"'\", '".join(parts_wo_apos)
        if '\'' in str:
            return "\"%s\"" % str
        return "'%s'" % str
