# (c) 2022 Warren Usui
# Squidly_dorkle
# This code is licensed under the MIT license (see LICENSE.txt for details)
"""
Interface to test sedecordle solving code against a specific setup
"""
import os
from utilities import extract_data
from brainz import solve_it

from simulator import SimInterface

class FileBackend(SimInterface):
    """
    Object that solver code in simulator.py uses to read word lists
    """
    def __init__(self):
        super().__init__()
        self.clue_list = self.get_next()
        self.delay = 0

    def get_next(self):
        """
        Randomly set up a new set of words.
        """
        with open(os.sep.join(["data", "ztest.txt"]), 'r',
                  encoding="UTF-8") as infile:
            indata = infile.read()
        self.clue_list = indata.split()
        return self.clue_list[:]

if __name__ == "__main__":
    extract_data('answers')
    if os.path.exists(os.sep.join(["data", "ztest.txt"])):
        solve_it(FileBackend())
