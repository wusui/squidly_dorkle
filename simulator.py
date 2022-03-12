# (c) 2022 Warren Usui
# Squidly_dorkle
# This code is licensed under the MIT license (see LICENSE.txt for details)
"""
Simulation interface. Used by test code to rerun specific word layouts, and by a random game
generator so that a lot of tests can be run.
"""
import os
import json
class SimInterface():
    """
    Sedecordle simulator.  Useful for testing, debugging, and code exercising.

    @param back_end object word supplier object
    @param runs integer number of times to run this
    """
    def __init__(self):
        self.yg_patterns = [ [] for _ in range(0, 16)]
        self.input = []
        self.clue_list = []

    def add_word(self, word):
        """
        A word has been added. Change internal data and add new pattern

        @param String word word to be added
        """
        for indx in range(0, 16):
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

    def identify_if_solved(self):
        """
        Return "solved" if puzzle is solved, unsolved if at least one word
        is not all green.
        """
        for indx in range(0, 16):
            if self.yg_patterns[indx][-1] != "GGGGG":
                return "unsolved"
        return "solved"

    def chk_word_in_grid(self, word, limitv):
        """
        Get pattern for this word nuumber
        """
        return self.yg_patterns[word - 1][0:limitv - 1]

    def shutdown(self):
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

def eval_guess(cword, guess):
    """
    Compare a word with a guess.  Return the YG pattern

    @param cword String Word we are testing against
    @param guess String Word we are guessing
    @return YG pattern for this pair
    """
    pass1 = []
    for indx, letter in enumerate(cword):
        if letter == guess[indx]:
            pass1.append("G")
        else:
            pass1.append(".")
    wyellow = {}
    gyellow = {}
    for letr in "abcdefghijklmnopqrstuvwxyz":
        wyellow[letr] = 0
        gyellow[letr] = 0
    for indx, letter in enumerate(guess):
        if pass1[indx] != 'G':
            wyellow[cword[indx]] = wyellow.get(cword[indx], 0) + 1
            gyellow[letter] = gyellow.get(letter, 0) + 1
    pass2 = []
    for indx, letter in enumerate(guess):
        if pass1[indx] == 'G':
            pass2.append('G')
        else:
            if wyellow[letter] > 0 and gyellow[letter] > 0:
                pass2.append('Y')
                wyellow[letter] -= 1
                gyellow[letter] -= 1
            else:
                pass2.append('.')
    return ''.join(pass2)
