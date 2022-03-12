# (c) 2022 Warren Usui
# Squidly_dorkle
# This code is licensed under the MIT license (see LICENSE.txt for details)
"""
Interface to test sedecordle solving code using game data specified in a file
"""
import os

from simulator import SimInterface

class TestBackend(SimInterface):
    """
    Object that solver code in brainz.py uses to inteface with data in a file
    """
    def __init__(self):
        with open(os.sep.join(["data", "test.txt"]), "r",
                  encoding="utf8") as infile:
            indata = infile.read()
        parts = indata.split("\n")
        self.data = []
        for row in parts:
            self.data.append(row.split(","))
        self.runs = self.get_rcount(100)
        super().__init__()
        self.clue_list = self.get_next()
        self.delay = 0

    def get_rcount(self,runs):
        """
        Return the lesser of the number of runs specified by the runs
        parameter or the number of runs that are in the test.txt file.

        @param runs Integer number of runs specified by the user
        @return Integer number of runs we are testing
        """
        if len(self.data) < runs:
            return len(self.data)
        return runs

    def get_next(self):
        """
        Return the words in the next line of the file as the next game
        values.
        """
        if not self.data:
            return self.data
        retv = self.data[0]
        self.data = self.data[1:]
        self.clue_list = retv
        return retv
