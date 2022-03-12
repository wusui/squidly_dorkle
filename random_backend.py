# (c) 2022 Warren Usui
# Squidly_dorkle
# This code is licensed under the MIT license (see LICENSE.txt for details)
"""
Interface to test sedecordle solving code by simulating random picks from
the website
"""
import random

from simulator import SimInterface

class RandomBackend(SimInterface):
    """
    Object that solver code in brainz.py uses to inteface with data in a file
    """
    def __init__(self, runs):
        super().__init__()
        self.runs = runs
        with open("answers.txt", "r", encoding="UTF-8") as f_file:
            ostr = f_file.read()
        self.wordlist = ostr.split()
        self.clue_list = self.get_next()
        self.delay = 0

    def get_rcount(self,runs):
        """
        Return the lesser of the number of runs specified by the runs
        parameter or MAXLIMIT

        @param runs Integer number of runs specified by the user
        @return Integer number of runs we are testing
        """
        MAXLIMIT = 100000
        if runs < MAXLIMIT:
            return runs
        return MAXLIMIT

    def get_next(self):
        """
        Return the words in the next line of the file as the next game
        values.
        """
        random.shuffle(self.wordlist)
        self.clue_list = self.wordlist[0:16]
        return self.clue_list[:]
