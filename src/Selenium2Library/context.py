# TODO: Move back to base when updating ElementFinder use ctx
class ContextAware(object):

    def __init__(self, ctx):
        self.ctx = ctx

    @property
    def browser(self):
        return self.ctx._browser

    @property
    def browsers(self):
        return self.ctx._browsers
