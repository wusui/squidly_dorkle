# (c) 2022 Warren Usui
# Squidly_dorkle
# This code is licensed under the MIT license (see LICENSE.txt for details)
"""
Solving engine for squidly_dorkle
"""
import os
from datetime import datetime

STARTER = ["raise"]

class Solver():
    """
    Solver object

    input       -- list of guesses made so far
    wordtable   -- all possible answers
    wordlists   -- list of word lists (one for each of the 16 words to guess)
    """
    def __init__(self, delay=0):
        self.input = []
        self.wordtable = get_words("answers.txt")
        self.wordlists = []
        self.starter = STARTER[:]
        self.closer = ["gamma"]
        for _ in range(16):
            self.wordlists.append(self.wordtable[:])
        self.delay = delay
        fname = datetime.now().strftime("errorlog-%Y-%m-%d-%H-%M-%S")
        self.elog = os.sep.join(["data", fname])

    def make_guess(self, guess, gm_interface):
        """
        Enter a guess.  Handle results if a word is solved.  If not,
        update each wordlist based on the response from gm_interface

        @param guess string 5 letter word guessed
        @param gm_interface Interface (either web-site or simulator)

        self.wordlists get updated
        """
        gm_interface.add_word(guess)
        self.input.append(guess)
        for windx in range(16):
            if self.wordlists[windx] == []:
                continue
            ygpattern = gm_interface.chk_word_in_grid(windx + 1)
            if ygpattern[-1] == "GGGGG":
                self.wordlists[windx] = []
                continue
            self.wordlists[windx] = reduce_list(
                guess, self.wordlists[windx], ygpattern[-1])

    def not_done(self):
        """
        Return True if all wordlists are not completely solved
        """
        for wlist in self.wordlists:
            if wlist:
                return True
        return False

    def get_word_data(self):
        """
        Collect all the words from the wordlist and return a count of
        letter usage and the collected word list

        @return hist, wordg -- letter histogram and word list.
        """
        hist = {}
        wordg = []
        for lst in self.wordlists:
            for wrd in lst:
                wordg.append(wrd)
                for ltr in wrd:
                    if ltr in hist:
                        hist[ltr] += 1
                    else:
                        hist[ltr] = 1
        for wrd in self.input:
            if len(self.input) > 21:
                print("ERROR: took over 21 words")
            for ltr in wrd:
                hist[ltr] = 0
        return hist, wordg

    def find_bestword(self):
        """
        Find a word with five different letters that uses the most letters
        in unmatched word lists so far.

        @return best word (uses most letters in unmatched word list. Has
                five different letters).
        """
        hist, wordg = self.get_word_data()
        bestnumb = 0
        bestword = ""
        for word in wordg:
            if len(set(word)) != 5:
                continue
            mynumb = 0
            for letter in word:
                if letter in hist:
                    mynumb += hist[letter]
            if mynumb > bestnumb:
                bestnumb = mynumb
                bestword = word
        if bestword == "":
            for wurd in wordg:
                if wurd not in self.input:
                    bestword = wurd
                    break
        return bestword

    def real_brains(self, gm_interface):
        """
        Check the words in the grid against the intial guesses
        Changes new_entries and dup_word values.

        @param solver object Solver class object
        """
        while self.not_done():
            found_one = False
            for wval in range(16):
                if len(self.wordlists[wval]) == 1:
                    self.make_guess(self.wordlists[wval][0], gm_interface)
                    found_one = True
                    break
            if found_one:
                continue
            if self.starter:
                self.make_guess(self.starter[0], gm_interface)
                self.starter = self.starter[1:]
            else:
                bestword = self.find_bestword()
                self.make_guess(bestword, gm_interface)

def check_word(guess, tword, ygpattern):
    """
    Given a guess, a word, and a pattern for the guess, evaluate
    the word based on the guess and the YG-pattern

    @param guess string Word Guessed
    @param tword word to be tested
    @param ygpattern string 5-character YG pattern
    @return True if word should not be in list.
    """
    for indx, _ in enumerate(tword):
        bad_bit = True
        if ygpattern[indx] == ".":
            if guess[indx] in tword:
                chk = 0
                for wcnt in range(5):
                    if guess[wcnt] == guess[indx]:
                        chk += 1
                if chk == 1:
                    break
        if ygpattern[indx] == "G":
            if guess[indx] != tword[indx]:
                break
        if ygpattern[indx] == "Y":
            if guess[indx] not in tword:
                break
            if guess[indx] == tword[indx]:
                break
        bad_bit = False
    return bad_bit

def reduce_list(guess, wlist, ygpattern):
    """
    Given a guess, a wordlist, and a pattern for the guess, prune entries
    from the wordlist based on the guess and the YG-pattern

    @param guess string Word Guessed
    @param wlist list Words that are still possible solutions
    @param ygpattern string 5-character YG pattern
    @return new wlist value
    """
    nlist = []
    for tword in wlist:
        if not check_word(guess, tword, ygpattern):
            nlist.append(tword)
    return nlist

def get_words(wlist):
    """
    Extract words from a file.

    @param wlist String name of file to read
    @return list List of all possible answer words (strings)
    """
    with open(wlist, "r", encoding="UTF-8") as f_file:
        ostr = f_file.read()
    return ostr.split()

def solve_it(gm_interface):
    """
    Main solving routine. Make sure files are set up,call real_brains
    and record the results

    @param gm_interface object Interface used (webpage, debugger,
           or simulator)
    """
    if not os.path.exists("data"):
        os.mkdir("data")
    solvr = Solver()
    solvr.real_brains(gm_interface)
    print(len(solvr.input), solvr.input)
    gm_interface.shutdown(len(solvr.input))
