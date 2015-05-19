import events as event
from robot.api import logger

class LibraryListener(object):

    ROBOT_LISTENER_API_VERSION = 2

    def start_suite(self, name, attrs):
        event.dispatch( 'scope_start', attrs['longname'] )

    def end_suite(self, name, attrs):
        event.dispatch( 'scope_end', attrs['longname'] )

    def start_test(self, name, attrs):
        event.dispatch( 'scope_start', attrs['longname'] )

    def end_test(self, name, attrs):
        event.dispatch( 'scope_end', attrs['longname'] )
