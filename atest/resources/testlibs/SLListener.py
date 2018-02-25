from robot.api import logger


class SLListener(object):

    ROBOT_LISTENER_API_VERSION = 2

    kw_name = ''

    def start_keyword(self, name, attributes):
        self.kw_name = name
        logger.console('Keyword start: {}'.format(name))

    def end_keyword(self, name, attributes):
        logger.console('Keyword stop {}'.format(name))
        self.kw_name = ''

    def log_message(self, message):
        logger.console('Keyword {} messages'.format(self.kw_name))
        logger.console('{}'.format(message))
