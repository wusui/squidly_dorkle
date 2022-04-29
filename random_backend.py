# (c) 2022 Warren Usui
# Squidly_dorkle
# This code is licensed under the MIT license (see LICENSE.txt for details)
"""
Interface to test sedecordle solving code by simulating random picks from
the website
"""
import random
from configparser import ConfigParser
from simulator import SimInterface
from simulator import show_stats
from utilities import extract_data, NUM_TO_SOLVE
from brainz import solve_it

class RandomBackend(SimInterface):
    """
    Object that solver code in simulator.py uses to create random word lists
    """
    def __init__(self, cnt, perfbit=False, start_word="raise"):
        super().__init__()
        with open("answers.txt", "r", encoding="UTF-8") as f_file:
            ostr = f_file.read()
        self.wordlist = ostr.split()
        self.clue_list = self.get_next(perfbit, start_word)
        self.count = cnt
        self.delay = 0
        self.find_perfection = perfbit

    def get_next(self, perfbit, start_word):
        """
        Randomly set up a new set of words.
        """
        random.shuffle(self.wordlist)
        self.clue_list = self.wordlist[0:NUM_TO_SOLVE]
        foundit = False
        if perfbit:
            for aword in self.clue_list:
                if  aword == start_word:
                    foundit = True
                    break
            if not foundit:
                self.clue_list[0] = start_word
        return self.clue_list[:]

def run_sim(sim_numb, word='raise', perfbit=False, hurry=True):
    """
    Wrapper to run the random puzzle simulator a number of times.

    @param sim_numb number of times to run the simulation
    """
    for cnt in range(sim_numb):
        solve_it(RandomBackend(cnt, perfbit=perfbit, start_word=word),
                 start_word=word, hurry=hurry)
    show_stats(sim_numb)

def sim_interface():
    """
    Simulator interface to also use the config file
    """
    extract_data('answers')
    config = ConfigParser()
    config.read('config.ini')
    parse_info = config["DEFAULT"]
    runs = int(parse_info["runs"])
    start_word = parse_info["start"]
    perfbit = parse_info["seek_perfection"] == "True"
    hurry = True
    if perfbit:
        hurry = False
    run_sim(runs, word=start_word, perfbit=perfbit, hurry=hurry)

if __name__ == "__main__":
    sim_interface()
