from robot.api import logger


class Base(object):

    def info(self, msg, html=False):
        logger.info(msg, html)

    def debug(self, msg, html=False):
        logger.debug(msg, html)

    def log(self, msg, level='INFO', html=False):
        logger.write(msg, level, html)

    def warn(self, msg, html=False):
        logger.warn(msg, html)
