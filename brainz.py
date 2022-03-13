# (c) 2022 Warren Usui
# Squidly_dorkle
# This code is licensed under the MIT license (see LICENSE.txt for details)
"""
Solving engine for squidly_dorkle
"""
import os
from datetime import datetime
from time import sleep

STARTER = ["blade", "comfy", "right", "spunk"]

class Solver():
    """
    Solver object

    gm_inf      -- link to game interface (selenium webpage handler,
                   simulator, or tester
    input       -- list of guesses made so far
    new_entries -- dict indexed by position in the puzzle of solved words
    dup_words   -- dict indexed by position in the puzzle of unsolved lists
    guess_list  -- allowed guesses
    wordtable   -- all possible answers
    """
    def __init__(self, delay=0):
        self.input = []
        self.new_entries = {}
        self.dup_words = {}
        self.guess_list = get_words("allowed.txt")
        self.wordtable = do_scan(STARTER, get_words("answers.txt"))
        self.delay = delay
        fname = datetime.now().strftime("errorlog-%Y-%m-%d-%H-%M-%S")
        self.elog = os.sep.join(["data", fname])

    def real_brains(self, gm_interface):
        """
        Check the words in the grid against the intial guesses
        Changes new_entries and dup_word values.

        @param solver object Solver class object
        """
        for word in STARTER:
            gm_interface.add_word(word)
        for word in range(1, 17):
            indx = gm_interface.chk_word_in_grid(word, 5)
            tindex = '|'.join(indx)
            if "GGGGG" in tindex:
                continue
            if len(self.wordtable[tindex]) == 1:
                gm_interface.add_word(self.wordtable[tindex][0])
                self.new_entries[word] = self.wordtable[tindex][0]
            else:
                self.dup_words[word] = self.wordtable[tindex]
        if len(self.dup_words) > 0:
            if self.handle_dup_cases(gm_interface):
                self.handle_dup_cases(gm_interface)

    def handle_dup_cases(self, gm_interface):
        """
        At this point, scan all the unsolved words against later guesses
        """
        while len(self.dup_words) > 0:
            nwd = {}
            for entry in self.dup_words:
                answ = self.eval_next_lv(gm_interface, entry)
                if len(answ) == 1:
                    gm_interface.add_word(answ[0])
                    self.new_entries[entry] = answ[0]
                else:
                    nwd[entry] = answ
            if wsize(self.dup_words) == wsize(nwd):
                break
            if wsize(self.dup_words) > wsize(nwd):
                self.dup_words = nwd.copy()
        if len(self.dup_words) > 0:
            self.scan_for_disamb(gm_interface)
            with open(self.elog, "a", encoding="UTF-8") as fdesc:
                fdesc.write(", ".join(gm_interface.clue_list) + "\n")
                for ent in self.dup_words:
                    if len(self.dup_words[ent]) > 0:
                        fdesc.write("     " + ", ".join(self.dup_words[ent]) +
                                                        "\n")
            gm_interface.shutdown()
        return False

    def scan_for_disamb(self, gm_interface):
        """
        Check allowed words to see if there is one that uniquely
        causes all dup_words to be disambiguated.

        @param gm_interface object interface
        @return True if good guess found, false if not
        """
        for chkword in self.guess_list:
            okay = True
            for indx in self.dup_words:
                if not wcheckout(chkword, self.dup_words[indx]):
                    okay = False
                    break
            if okay:
                gm_interface.add_word(chkword)
                return True
        return False

    def eval_next_lv(self, gm_interface, entry):
        """
        Evaluate the word list against all information in the grid

        @param integer entry index into the sedecordle grid
        @return list updated list of possible words
        """
        gpat = 5 * [""]
        ypat = 5 * [""]
        unused = ""
        for indx, sptrn in enumerate(gm_interface.chk_word_in_grid(entry, 22)):
            maybebad = ""
            for indx2, spce in enumerate(sptrn):
                lchar = gm_interface.input[indx][indx2]
                if spce == "Y":
                    if lchar not in ypat[indx2]:
                        ypat[indx2] += lchar
                if spce == "G":
                    gpat[indx2] = lchar
                if spce == ".":
                    if lchar not in unused:
                        maybebad += lchar
            unused += addbad(indx, sptrn, maybebad, gm_interface)
        ans_list = []
        for word in self.dup_words[entry]:
            if not check_b4_adding(word, gpat, ypat, unused):
                ans_list.append(word)
        return ans_list

def addbad(indx, sptrn, maybebad, gm_interface):
    """
    Add to the unused character list

    @param integer indx index into the sedecordle word grid
    @param String sptrn word information from word grid
    @param String maybebad potentially bad letters
    @return String unused letters
    """
    letsunused = ""
    for lchr in maybebad:
        bad = True
        for indx2, spce in enumerate(sptrn):
            if spce != ".":
                if gm_interface.input[indx][indx2] == lchr:
                    bad = False
        if bad:
            letsunused += lchr
    return letsunused

def check_guess(word, guess):
    """
    Compare a word with a guess

    @param word String Word being checked
    @param guess String Word being guessed
    @return String Green/Yellow/Black letter indication pattern
    """
    retv = ''
    for indx, letter in enumerate(word):
        if guess[indx] == letter:
            retv += 'G'
        else:
            if guess[indx] in word:
                retv += 'Y'
            else:
                retv += '.'
    return retv

def gen_key(word, guesses):
    """
    Take guess results (Y/G/B patterns) and return a string to use as
    part of a key to index all words

    @param word String assumed word
    @param guesses list List of guesses
    """
    nkeys = []
    for guess in guesses:
        nkeys.append(check_guess(word, guess))
    return "|".join(nkeys)

def do_scan(wlist, anlist):
    """
    Scan a list of words for matches in another list

    @param wlist List Words to be guessed
    @param list of possible answer words
    @return dict Dictionary indexed by gen_key values of words corresponding
                 to that pattern
    """
    big_table = {}
    for wrd in anlist:
        tindx = gen_key(wrd, wlist)
        if tindx not in big_table:
            big_table[tindx] = [wrd]
        else:
            big_table[tindx].append(wrd)
    return big_table

def get_words(wlist):
    """
    Extract words from a file.

    @param wlist String name of file to read
    @return list List of all possible answer words (strings)
    """
    with open(wlist, "r", encoding="UTF-8") as f_file:
        ostr = f_file.read()
    return ostr.split()

def check_b4_adding(word, gpat, ypat, unused):
    """
    Return True if:
        gpat indicates that a letter is green and a letter does not match
        ypat indicates that a letter is yellow and this letter matches or
            this letter is not found in the word
        the letter matches a letter known to be unused

    @param word String word to check
    @param gpat String Green pattern
    @param ypat String yellow pattern
    @param unused String unused letters
    @return True/False
    """
    bad = False
    for indx, letter in enumerate(gpat):
        if letter != '':
            if letter != word[indx]:
                return True
    for indx, ylets in enumerate(ypat):
        if ylets != '':
            for ltr in ylets:
                if ltr == word[indx]:
                    return True
                if ltr not in word:
                    return True
    for letter in word:
        if letter in unused:
            bad = True
            break
    return bad

def wsize(dict_o_lists):
    """
    Count the number of entries in the list values of a dictionary

    @param dictionary dictionary with lists as values
    @return int Total number of entries in all lists
    """
    counter = 0
    for entry in dict_o_lists:
        counter += len(dict_o_lists[entry])
    return counter

def wcheckout(guess, patterns):
    """
    Call get_yg_val for all words that we want to check.  Return true
    if all the YG patterns are unique (guaranteeing that we can make a
    correct guess for all words after this one)

    @param guess String word to guess
    @param patterns list of strings that we want to make sure form unique
           patterns
    @return True if all words in patterns are unique
    """
    yglist = []
    for poss_word in patterns:
        yglist.append(get_yg_val(poss_word, guess))
    if len(set(yglist)) == len(patterns):
        return True
    return False

def get_yg_val(poss_word, guess):
    """
    Generate the YG pattern for a guess so that we can compare words with
    information from the sedecordle output

    @param poss_word String word we assume to be the sedecordle word
    @param guess String a word we are comparing poss_word with
    @return String Yellow/Green/Black output from this comparison
    """
    yg_str = ""
    for indx, letter in enumerate(poss_word):
        if letter == guess[indx]:
            yg_str += "G"
        else:
            yg_str += "."
    nong = ""
    for indx, letter in enumerate(poss_word):
        if yg_str[indx] != "G":
            nong += letter
    for indx, letter in enumerate(poss_word):
        if letter != guess[indx]:
            if letter in nong:
                yg_str = yg_str[:indx] + "Y" + yg_str[indx + 1:]
    return yg_str

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
    for _ in range(0, gm_interface.runs):
        solvr.real_brains(gm_interface)
        print(gm_interface.input)
        gm_interface.input = []
        gm_interface.dup_words = {}
        gm_interface.new_entries = {}
        gm_interface.yg_patterns = [ [] for _ in range(0, 16)]
        if gm_interface.runs > 1:
            gm_interface.clue_list = gm_interface.get_next()
    sleep(gm_interface.delay)
    gm_interface.shutdown()
