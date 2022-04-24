# (c) 2022 Warren Usui
# Squidly_dorkle
# This code is licensed under the MIT license (see LICENSE.txt for details)
"""
Interface to test sedecordle solving code by simulating random picks from
the website
"""
import random

from simulator import SimInterface
from simulator import show_stats
from utilities import extract_data, NUM_TO_SOLVE
from brainz import solve_it

class RandomBackend(SimInterface):
    """
    Object that solver code in simulator.py uses to create random word lists
    """
    def __init__(self, cnt):
        super().__init__()
        with open("answers.txt", "r", encoding="UTF-8") as f_file:
            ostr = f_file.read()
        self.wordlist = ostr.split()
        self.clue_list = self.get_next()
        self.count = cnt
        self.delay = 0
        self.guess_count = 0
        self.find_perfection = False

    def get_next(self):
        """
        Randomly set up a new set of words.
        """
        random.shuffle(self.wordlist)
        self.clue_list = self.wordlist[0:NUM_TO_SOLVE]
        return self.clue_list[:]

def run_sim(sim_numb, word='raise'):
    """
    Wrapper to run the random puzzle simulator a number of times.

    @param sim_numb number of times to run the simulation
    """
    for cnt in range(sim_numb):
        solve_it(RandomBackend(cnt), start_word=word)
    show_stats(sim_numb)

if __name__ == "__main__":
    extract_data('answers')
    run_sim(100)
