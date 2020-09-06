import json
import os
import platform

from robot.api import logger


class BigListOfNaughtyStrings:
    """The  Big List of Naughty Strings is originally copied from here:
    https://github.com/minimaxir/big-list-of-naughty-strings
    """

    def get_blns(self):
        if platform.system() == "Windows":
            logger.warn(
                "Rading Big List of Naughty Strings does not work in Windows OS"
            )
            return []
        cur_dir = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(cur_dir, "blns.json")) as blns:
            return json.load(blns)
