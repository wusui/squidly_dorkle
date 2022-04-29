# (c) 2022 Warren Usui
# Squidly_dorkle
# This code is licensed under the MIT license (see LICENSE.txt for details)
"""
Interface to the sedecordle webpage
"""
import os
from configparser import ConfigParser
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import chromedriver_autoinstaller
from utilities import extract_data, WEBSITE, MAX_GUESS_ALLOWED, NUM_TO_SOLVE
from brainz import solve_it, Solver

class WebInterface():
    """
    Sedecordle web interface.  Save the driver value and go to the free
    web page
    """
    def __init__(self, website, delay, perfbit=False):
        self.solver = Solver()
        chromedriver_autoinstaller.install()
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.driver = webdriver.Chrome(service=Service(), options=options)
        self.driver.get(website)
        self.driver.maximize_window()
        self.delay = delay
        sleep(self.delay // 2)
        elem1 = self.driver.find_element(By.ID, "free")
        elem1.click()
        sleep(self.delay // 2)
        self.input = []
        self.clue_list = ["data", "not", "found"]
        self.guess_count = 0
        self.find_perfection = perfbit

    def compute_disp_loc(self, word):
        """
        Find the most likely location where word would be a solution

        @param word String word passed to add_word
        @returns int 0 through 15 (index of wordlists we should use)
        """
        if len(self.solver.winput) < 2:
            return 0
        possible = [-1, 0]
        lsize = [5000, 5000]
        for indx in range(NUM_TO_SOLVE):
            llen = len(self.solver.wordlists[indx])
            if llen < lsize[1]:
                lsize[1] = llen
                possible[1] = indx
            if word in self.solver.wordlists[indx]:
                if llen == 1:
                    return indx
                if llen < lsize[0]:
                    lsize[0] = llen
                    possible[0] = indx
        if possible[0] >= 0:
            return possible[0]
        return possible[1]

    def add_word(self, word):
        """
        Add a word into the sedecordle grid.  Sends character by character
        data and saves the word in self.input

        @param word String word that is being guessed
        """
        inm = 1
        one_third_page = MAX_GUESS_ALLOWED // 3
        if len(self.solver.winput) > one_third_page:
            inm =  len(self.solver.winput) - one_third_page
        bnm = 2 * (self.compute_disp_loc(word) // 2) + 1
        element = self.driver.find_element(By.ID, f"box{bnm},{inm},1")
        self.driver.execute_script("arguments[0].scrollIntoView();",
                                       element)
        self.input.append(word)
        for letter in word:
            elem = self.driver.find_element(By.ID, letter)
            elem.click()
        elem = self.driver.find_element(By.ID, "enter2")
        elem.click()
        self.guess_count += 1

    def chk_word_in_grid(self, word):
        """
        Extract the color (Yellow/Green) information from words in the grid

        @param int word number of word to check
        """
        indx = []
        for guess in range(1, 25):
            bcheck = self.driver.find_element(
                By.ID, f"box{word},{guess},1").text
            if bcheck == '':
                break
            boxes = []
            for letter in range(1, 6):
                bkgrnd = self.driver.find_element(
                    By.ID, f"box{word},{guess},{letter}"
                    ).get_attribute("style")
                if "(24, " in bkgrnd:
                    boxes.append(".")
                if "(255, " in bkgrnd:
                    boxes.append("Y")
                if "(0, " in bkgrnd:
                    boxes.append("G")
            indx.append(''.join(boxes))
        return indx

    def shutdown(self, score):
        """
        Save a screen shot and exit
        """
        if score == 16 or not self.find_perfection:
            self.driver.get_screenshot_as_file(
                os.sep.join(["data", f"screenshot{score}.png"]))
            sleep(self.delay)
        self.driver.quit()

def use_website():
    """
    Main module.  Get parameters from config.ini.  Runs is the number
    of times we should run.  Seek_perfection, when true, terminates after
    we know we can't  have a perfect run.
    """
    extract_data('answers')
    config = ConfigParser()
    config.read('config.ini')
    parse_info = config["DEFAULT"]
    runs = int(parse_info["runs"])
    delay = int(parse_info["delay"])
    start_word = parse_info["start"]
    pbit = False
    seek_perfection = parse_info["seek_perfection"]
    if seek_perfection == "True":
        pbit = True
    for _ in range(runs):
        solver = WebInterface(WEBSITE, delay=delay, perfbit=pbit)
        if pbit:
            solution = solve_it(solver, start_word=start_word, hurry=False)
        else:
            solution = solve_it(solver, start_word=start_word)
        if solver.find_perfection and solution >= 16:
            solver.delay = 10
            break

if __name__ =="__main__":
    use_website()
