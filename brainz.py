# (c) 2022 Warren Usui
# Squidly_dorkle
# This code is licensed under the MIT license (see LICENSE.txt for details)
"""
Solving engine for squidly_dorkle
"""
import os
from datetime import datetime
from utilities import eval_guess, MAX_GUESS_ALLOWED, WORD_SIZE, NUM_TO_SOLVE

class Solver():
    """
    Solver object

    winput       -- list of guesses made so far
    wordtable   -- all possible answers
    wordlists   -- list of word lists (one for each of the 16 words to guess)
    """
    def __init__(self, pstart="raise", hurry=True):
        self.winput = []
        self.wordtable = get_words("answers.txt")
        self.wordlists = []
        self.starter = [pstart]
        for _ in range(NUM_TO_SOLVE):
            self.wordlists.append(self.wordtable[:])
        #self.delay = delay
        fname = datetime.now().strftime("errorlog-%Y-%m-%d-%H-%M-%S")
        self.elog = os.sep.join(["data", fname])
        self.guess2 = True
        self.hurry = hurry

    def make_guess(self, guess, gm_interface):
        """
        Enter a guess.  Handle results if a word is solved.  If not,
        update each wordlist based on the response from gm_interface

        @param guess string 5 letter word guessed
        @param gm_interface Interface (either web-site or simulator)

        self.wordlists get updated
        """
        gm_interface.add_word(guess)
        self.winput.append(guess)
        for windx in range(NUM_TO_SOLVE):
            if guess in self.wordlists[windx]:
                self.wordlists[windx].remove(guess)
        for windx in range(NUM_TO_SOLVE):
            if self.wordlists[windx] == []:
                continue
            ygpattern = gm_interface.chk_word_in_grid(windx + 1)
            if ygpattern[-1] == "GGGGG":
                self.wordlists[windx] = []
                continue
            self.wordlists[windx] = reduce_list(
                guess, self.wordlists[windx], ygpattern[-1])
        solvedwlcnt = 0
        for indiv_wl in self.wordlists:
            if indiv_wl == []:
                solvedwlcnt += 1
        if solvedwlcnt < gm_interface.guess_count:
            if gm_interface.find_perfection:
                self.wordlists = []

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
        for wrd in self.winput:
            for ltr in wrd:
                hist[ltr] = 0
        return hist, wordg

    def nittygritty(self, wordg):
        """
        At this point, handle the cases where we should try to find words
        that eliminate as many of the possible words left.  This will only
        run once there are fewer than 21 words, and the purpose here is to
        eliminaate as many words as possible with each guess.

        @param wordg list of remaining words
        """
        best_worst_case = len(wordg)
        best_words = [wordg[0]]
        for tword in self.wordtable:
            best_word_bwc = 0
            for indx in range(NUM_TO_SOLVE):
                if not self.wordlists[indx]:
                    continue
                wdist = {}
                for word in self.wordlists[indx]:
                    pattern = eval_guess(word, tword)
                    if pattern in wdist:
                        wdist[pattern] += 1
                    else:
                        wdist[pattern] = 1
                wmax = 0
                for elem in wdist.items():
                    if elem[1] > wmax:
                        wmax = elem[1]
                best_word_bwc += wmax
            if best_word_bwc < best_worst_case:
                best_worst_case = best_word_bwc
                best_words = [tword]
            else:
                if best_word_bwc == best_worst_case:
                    best_words.append(tword)
        return self.select_word(best_words, wordg)

    def select_word(self, best_words, wordg):
        """
        Pick the right word.  Use possible solutions first

        @param best_words list of equivalent answers (as far as solutions
                          are concerned
        @param wordg possible words to pick that are still leftt
        @return next word to try
        """
        for word in best_words:
            if word in wordg:
                if word not in self.winput:
                    return word
        for word in best_words:
            if word not in self.winput:
                return word
        print("REALLY MESSED UP")
        return wordg[-1]

    def find_best5(self, hist, wordg):
        """
        Find the best guess with five different letters.

        @param hist, wordg -- return values from get_word_data()
        """
        bestnumb = 0
        bestword = ""
        if self.guess2:
            for word in wordg:
                if len(wordg) < MAX_GUESS_ALLOWED:
                    break
                if len(set(word)) != WORD_SIZE:
                    continue
                mynumb = 0
                for letter in word:
                    if letter in hist:
                        mynumb += hist[letter]
                if mynumb > bestnumb:
                    bestnumb = mynumb
                    bestword = word
        return bestword

    def find_bestword(self):
        """
        Find a word with five different letters that uses the most letters
        in unmatched word lists so far.  If none found, call nittygritty to
        get a solution.

        @return string next word to be guessed
        """
        hist, wordg = self.get_word_data()
        bestword = ""
        if self.hurry:
            bestword = self.find_best5(hist, wordg)
        if bestword == "":
            self.guess2 = False
            if self.winput[-1] == wordg[0]:
                for indx in range(NUM_TO_SOLVE):
                    if not self.wordlists[indx]:
                        continue
                    if self.wordlists[indx][0] == wordg[0]:
                        self.wordlists[indx] = self.wordlists[indx][1:]
            if len(wordg) == 2:
                return wordg[0]
            return self.nittygritty(wordg)
        return bestword

    def real_brains(self, gm_interface):
        """
        Check the words in the grid against the intial guesses
        Changes new_entries and dup_word values.

        @param solver object Solver class object
        """
        while self.not_done():
            found_one = False
            for wval in range(NUM_TO_SOLVE):
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

def handle_mult_letters(guess, tword, ygpattern, bad_bit):
    """
    Called from check_word to handle words with more than one of the
    same letter.  Parameters are the same except that bad_bit is
    passed and updated in some cases

    @return True if word should not be in the list
    """
    gval = {}
    gmax = {}
    wval = {}
    glim = {}
    for indx in range(WORD_SIZE):
        gmax.setdefault(guess[indx], 0)
        gmax[guess[indx]] += 1
        if ygpattern[indx] != '.':
            gval.setdefault(guess[indx], 0)
            gval[guess[indx]] += 1
        wval.setdefault(tword[indx], 0)
        wval[tword[indx]] += 1
    for chkr in gval.items():
        if gmax[chkr[0]] > chkr[1]:
            glim[chkr[0]] = chkr[1]
    for chkr in wval.items():
        if chkr[0] in glim:
            if chkr[1] > glim[chkr[0]]:
                bad_bit = True
    return bad_bit

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
                for wcnt in range(WORD_SIZE):
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
    return handle_mult_letters(guess, tword, ygpattern, bad_bit)

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

def solve_it(gm_interface, start_word='raise', hurry=True):
    """
    Main solving routine. Make sure files are set up,call real_brains
    and record the results

    @param gm_interface object Interface used (webpage, debugger,
           or simulator)
    """
    if not os.path.exists("data"):
        os.mkdir("data")
    solvr = Solver(pstart=start_word, hurry=hurry)
    gm_interface.solver = solvr
    solvr.real_brains(gm_interface)
    print(len(solvr.winput), solvr.winput)
    if len(solvr.winput) > MAX_GUESS_ALLOWED:
        with open("logfailures.txt", 'a', encoding="UTF-8") as errfile:
            answer = ", ".join(gm_interface.clue_list) + "\n"
            errfile.write(answer)
        print(gm_interface.clue_list)
    gm_interface.shutdown(len(solvr.winput))
    return len(solvr.winput)
