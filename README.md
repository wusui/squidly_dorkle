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

### Current state of the project

At this point, I need to figure out what the purpose of all this was.  My first goal was to write a sedecordle player that displays output to the screen.  Mission accomplished there, although I think that it would be cool to scroll the screen around so that the output looks more interesting.  Next I guess that there were two goals -- to play a sixteen move game and to never lose.  The sixteen move game is dependent on getting the first guess correct and will always be a crapshoot.  Running the simulator has demonstrated that it is possible to get a sixteen move game so I am fairly sure that as the code is right now it will eventually produce a sixteen move game on the web.

So now it's down to not losing.  I have been analyzing the output of the simulated losses and noticed that in some cases a guaranteed non-loss can happen if better guesses are made earlier.  These guesses guarantee a non-loss but also will not result in a sixteen move win either.  Since other games have generated sixteen move wins, I do not need to try for one here, so now my highest priority is not losing.

There are two word lists -- the answers list and the allowed word list.  The answers list is the list of possible words that sedecordle will use for words in the game, the allowed list is the list of words the user can guess.  Prior to this point, I have only used the answers list to guess a word because using a word not on the answers list would guarantee not solving the puzzle in 16 moves.  However, in the situation where I am trying to avoid losing, it may be the case that the best word to guesss is on the allowed list.  So I will probably now start using the allowed list in future guesses when there is no answer list word that will guarantee not losing.

### Links

[Sample simulation output of 1000 sedecordle games](http://www.warrensusui.com/toybox/squidly_dorkle/squidy_out1.txt)

[Sample recording of Sedecordle game run from Squidly_dorkle](http://www.warrensusui.com/toybox/squidly_dorkle/Squidly_dorkle_example1.mp4)

