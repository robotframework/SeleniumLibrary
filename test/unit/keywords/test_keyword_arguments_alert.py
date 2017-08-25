import unittest

from mockito import when, mock, verify, unstub

from SeleniumLibrary.keywords import AlertKeywords


TRUES = ['True', True, '1', 1, 'text']
FALSES = ['False', False, '', None, 'NONE']


class KeywordArgumentsAlertTest(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.alert = AlertKeywords(mock())

    def tearDown(self):
        unstub()

    def test_get_alert_message_dismiss_true(self):
        when(AlertKeywords)._handle_alert('dismiss').thenReturn('text')
        count = 1
        for true in TRUES:
            self.alert.get_alert_message(true)
            verify(AlertKeywords, times=count)._handle_alert('dismiss')
            count += 1
        self.alert.get_alert_message()
        verify(AlertKeywords, times=count)._handle_alert('dismiss')

    def test_get_alert_message_dismiss_false(self):
        when(AlertKeywords)._handle_alert().thenReturn('text')
        count = 1
        for false in FALSES:
            self.alert.get_alert_message(false)
            verify(AlertKeywords, times=count)._handle_alert()
            count += 1

    def test_dismiss_alert_true(self):
        when(AlertKeywords)._handle_alert('accept').thenReturn('text')
        count = 1
        for true in TRUES:
            self.alert.dismiss_alert(true)
            verify(AlertKeywords, times=count)._handle_alert('accept')
            count += 1
        self.alert.dismiss_alert()
        verify(AlertKeywords, times=count)._handle_alert('accept')

    def test_dismiss_alert_false(self):
        when(AlertKeywords)._handle_alert().thenReturn('text')
        count = 1
        for false in FALSES:
            self.alert.dismiss_alert(false)
            verify(AlertKeywords, times=count)._handle_alert()
            count += 1
