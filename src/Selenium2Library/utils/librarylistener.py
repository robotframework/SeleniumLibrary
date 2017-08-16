from .events import dispatch


class LibraryListener(object):
    ROBOT_LISTENER_API_VERSION = 2

    def start_suite(self, name, attrs):
        dispatch('scope_start', attrs['longname'])

    def end_suite(self, name, attrs):
        dispatch('scope_end', attrs['longname'])

    def start_test(self, name, attrs):
        dispatch('scope_start', attrs['longname'])

    def end_test(self, name, attrs):
        dispatch('scope_end', attrs['longname'])
