# (c) 2022 Warren Usui
# Squidly_dorkle
# This code is licensed under the MIT license (see LICENSE.txt for details)
"""
Stuff that writes files in this directory goes here
"""
from os.path import exists
import requests

WEBSITE = "http://sedecordle.com"
MAX_GUESS_ALLOWED = 21
WORD_SIZE = 5
NUM_TO_SOLVE = 16

def extract_data(field):
    """
    Write the allowed and answer files from data extracted from the
    sedecordle code

    @param field String file name (allowed or answers)
    """
    tfile = "".join([field, ".txt"])
    if exists(tfile):
        return
    from_loc = ''.join([field, ' = "'])
    wpage = requests.get(WEBSITE)
    tfront = str(wpage.content)
    first_str = tfront[tfront.find(from_loc):]
    ret_data = first_str[0:first_str.find('".split(')]
    with open(tfile, 'w', encoding="utf8") as fdesc:
        fdesc.write(ret_data[len(from_loc):])

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
