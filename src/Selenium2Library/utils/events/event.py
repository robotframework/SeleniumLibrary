from builtins import object
import abc

class Event(object):

    @abc.abstractmethod
    def trigger(self, *args, **kwargs):
        pass
