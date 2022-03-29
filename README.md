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

Module for keeping track of answers.txt and allowed.txt

##### mad_scientist_lab

Folder of experimental files run to help come up with some of the ideas
implemented

