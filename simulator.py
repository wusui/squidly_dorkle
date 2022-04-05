# (c) 2022 Warren Usui
# Squidly_dorkle
# This code is licensed under the MIT license (see LICENSE.txt for details)
"""
Simulation interface. Used by test code to rerun specific word layouts, and by a random game
generator so that a lot of tests can be run.
"""
import os
import json

from utilities import extract_data, eval_guess, MAX_GUESS_ALLOWED, NUM_TO_SOLVE

class SimInterface():
    """
    Sedecordle simulator.  Useful for testing, debugging, and code exercising.

    @param back_end object word supplier object
    @param runs integer number of times to run this
    """
    score_total = 0
    minscore = MAX_GUESS_ALLOWED
    maxscore = 0
    losses = 0
    def __init__(self):
        extract_data('allowed')
        extract_data('answers')
        self.yg_patterns = [ [] for _ in range(NUM_TO_SOLVE)]
        self.input = []
        self.clue_list = []
        self.solver = []

    def add_word(self, word):
        """
        A word has been added. Change internal data and add new pattern

        @param String word word to be added
        """
        for indx in range(NUM_TO_SOLVE):
            if len(self.yg_patterns[indx]) ==  0:
                self.add_pattern(indx, word)
            else:
                if self.yg_patterns[indx][-1] == "GGGGG":
                    continue
                self.add_pattern(indx, word)
        self.input.append(word)

    def add_pattern(self, indx, word):
        """
        Set new pattern using eval_guess.  Update yg_patterns

        @param index Integer word number in the puzzle (1 through 16)
        @param word String word to make pattern for
        """
        patt = eval_guess(self.clue_list[indx],  word)
        self.yg_patterns[indx].append(patt)

    def chk_word_in_grid(self, word):
        """
        Get pattern for this word number
        """
        return self.yg_patterns[word - 1]

    def shutdown(self, score):
        """
        Stash data before exiting
        """
        saved = {}
        saved["yg_patterns"] = self.yg_patterns
        saved["input"] = self.input
        ostr = json.dumps(saved)
        with open(os.sep.join(["data", "dump.json"]), "w",
                  encoding="utf8") as outfile:
            outfile.write(ostr)
        SimInterface.score_total += score
        SimInterface.minscore = min(score, SimInterface.minscore)
        SimInterface.maxscore = max(score, SimInterface.maxscore)
        if score > MAX_GUESS_ALLOWED:
            SimInterface.losses += 1

def show_stats(number):
    """
    Display stats

    @param number number of times we ran the simulation
    """
    average = SimInterface.score_total / number
    print(f"Average Score: {average:8.3f}")
    print(f"   Best Score: {SimInterface.minscore:4d}")
    print(f"  Worst Score: {SimInterface.maxscore:4d}")
    print(f"       Losses: {SimInterface.losses:4d}")

