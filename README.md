# squidly_dorkle

# Sedecordle solver

### INTRODUCTION
Runs on python after pip installing selenium and chromedriver_autoinstaller

This version decouples the selenium web logic from the actual game solving
logic.  Instead of using the web site, it is now possible to write game
drivers for simulations, stress tests, and debugging the game solving
logic for specific cases.

##### brainz.py

Main solving logic module

##### web_interface.py

Interface to the web page

##### file_io.py

Module for loading answers.txt and allowed.txt

##### simulator.py

Infrastructure to handle a simulator interface rather than using the website.  Used for testing brainz.py.

##### random_backend.py

Subclass of simulator that randomly assigns words to the puzzle grid.  This attempts to simulate the web page and runs must faster.

##### file_backend.py

Subclass of simulator that reads a file to assign words to the grid.  Used for debugging.

##### mad_scientist_lab

Folder of experimental files run to help come up with some of the ideas
implemented

### Current state of the code

Brainz.py currently guesses one word to start (RAISE).  If there is ever a point where one unsolved word only has one choice, then that choice is made.  If stuck, brainz.py then chooses a word from possible solutions that contains five different letters that attempts to decrease the lists of possible solutions by the greatest amount.  This step can happen more than once but usually only happens once.  If the puzzle is not solved by then, it tries to make a pick that eliminates as many possibilities across the remaining words, in order to avoid having to make potentially wrong guesses at the end.

The current code usually solves the puzzle in 18 guesses.  It now appears to pretty much solve all grids (it successfully solved 30,000 simulated grids without a failure).  Also, it finds a solution in 16 moves roughly once every 2,500 times.

The other thing to note is that all guesses so far use the answer list, not the available word list.  I've restricted this to answers because I want to improve the probability of getting a 16 guess solution.  For a first pass, this seems good.

### Links

[Sample simulation output of 1000 sedecordle games](http://www.warrensusui.com/toybox/squidly_dorkle/squidy_out1.txt)

[Sample recording of Sedecordle game run from Squidly_dorkle](http://www.warrensusui.com/toybox/squidly_dorkle/Squidly_dorkle_example1.mp4)
