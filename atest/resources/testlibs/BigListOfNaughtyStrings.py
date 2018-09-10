import json
import os


class BigListOfNaughtyStrings(object):
    """The  Big List of Naughty Strings is originally copied from here:
    https://github.com/minimaxir/big-list-of-naughty-strings
    """

    def get_blns(self):
        cur_dir = os.path.dirname(os.path.abspath(__file__))
        blns = open(os.path.join(cur_dir, 'blns.json'), 'r')
        return json.load(blns)
