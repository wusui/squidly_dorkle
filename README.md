# squidly_dorkle

# Sedecordle solver

### INTRODUCTION
Runs on python after pip installing selenium and chromedriver_autoinstaller

This version decouples the selenium web logic from the actual game solving
logic.  Instead of using the web site, it is now possible to write game
drivers for simulations, stress tests, and debugging the game solving
logic for specific cases.

##### main.py

Simple way to call this program

##### brainz.py

Main solving logic module

##### web_interface.py

Interface to the web page

##### file_io.py

Module for loading answers.txt and allowed.txt

##### simulator.py

Infrastructure to handle a simulator interface rather than using the website.  Used for testing brainz.py.

##### random_backend.py

Subclass of simulator that randomly assigns words to the puzzle grid.  This attempts to simulate the web page but runs must faster.  Other subclasses can be written if one wants to try other methods of testing the brainz.py logic.  For example, a tester that reads data from a file and uses that data as the initial word values can be used to test the code against specific situations.

##### mad_scientist_lab

Folder of experimental files run to help come up with some of the ideas
implemented

### Current state of the code

Brainz.py currently guesses one word to start (RAISE).  If there is ever a point where one unsolved word only has one choice, then that choice is made.  If stuck, brainz.py then chooses a word from possible solutions that contains five different letters that attempts to decrease the lists of possible solutions by the greatest amount.  This step can happen more than once but usually only happens once.  If the puzzle is not solved by then, the first available word that makes sense is picked.

The current code usually solves the puzzle in 18 guesses.  Approximately once every 2,500 times it fails to find the solution in 21 guesses.  Also, it finds a solution in 16 moves about the same number of times (roughly once every 2,500 times).

The guessing at the end could probably be improved to avoid going over 21 guesses.  Many of the layouts where this happens has multiple occurences of the same sets of words.  Frequently in these cases I see DROOL vs. DROLL, GRAVE vs. GRAZE, BOBBY vs. BOOBY vs. BOOZY, and GAMMA vs. MAGMA vs. MAMMA guesses.  More intelligent picking in these cases would probably solve a lot of problems but prior to this point, did not seem worth the effort.  I probably will work on improving these picks but the program works well in over 99.9% of the cases now anyway.

The other thing to note is that all guesses so far use the answer list, not the available word list.  I've restricted this to answers because I want to improve the probability of getting a 16 guess solution.  For a first pass, this seems good.

### Links


