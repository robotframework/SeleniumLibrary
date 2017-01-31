import abc
from builtins import object


class Event(object):

    @abc.abstractmethod
    def trigger(self, *args, **kwargs):
        pass
