class AttrDict(dict):

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)

    def __setattr__(self, name, value):
        self[name] = value

    def __delattr__(self, name):
        try:
            del self[name]
        except KeyError:
            raise AttributeError(name)

    def __eq__(self, other):
        return dict.__eq__(self, other)

    def __str__(self):
        return '{%s}' % ', '.join('%r: %r' % item for item in self.iteritems())

    # Must use original dict.__repr__ to allow customising PrettyPrinter.
    __repr__ = dict.__repr__
