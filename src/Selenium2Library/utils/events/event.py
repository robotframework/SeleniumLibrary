import abc

class Event(object):

    @abc.abstractmethod
    def trigger(self, *args, **kwargs):
        pass
