import os
import sys
from robot.api import logger
from keywordgroup import KeywordGroup
from robot.libraries.BuiltIn import BuiltIn

class _LoggingKeywords(KeywordGroup):

    # Private

    def _debug(self, message):
        logger.debug(message)

    def _get_log_dir(self):
        variables = BuiltIn().get_variables()

        logfile = variables['${LOG FILE}']
        if logfile != 'NONE':
            return os.path.dirname(logfile)
        return variables['${OUTPUTDIR}']

    def _html(self, message):
        logger.info(message, True, False)

    def _info(self, message):
        logger.info(message)

    def _log(self, message, level='INFO'):
        level = level.upper()
        if (level == 'INFO'): self._info(message)
        elif (level == 'DEBUG'): self._debug(message)
        elif (level == 'WARN'): self._warn(message)
        elif (level == 'HTML'): self._html(message)

    def _log_list(self, items, what='item'):
        msg = ['Altogether %d %s%s.' % (len(items), what, ['s',''][len(items)==1])]
        for index, item in enumerate(items):
            msg.append('%d: %s' % (index+1, item))
        self._info('\n'.join(msg))
        return items

    def _warn(self, message):
        logger.warn(message)
