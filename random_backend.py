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
    Object that solver code in simulator.py uses to create random word lists
    """
    def __init__(self):
        super().__init__()
        with open("answers.txt", "r", encoding="UTF-8") as f_file:
            ostr = f_file.read()
        self.wordlist = ostr.split()
        self.clue_list = self.get_next()
        self.delay = 0

    def get_next(self):
        """
        Return the words in the next line of the file as the next game
        values.
        """
        random.shuffle(self.wordlist)
        self.clue_list = self.wordlist[0:16]
        return self.clue_list[:]
