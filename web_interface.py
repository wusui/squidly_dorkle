# (c) 2022 Warren Usui
# Squidly_dorkle
# This code is licensed under the MIT license (see LICENSE.txt for details)
"""
Interface to the sedecordle webpage
"""
import os
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import chromedriver_autoinstaller
from file_io import extract_data, WEBSITE
from brainz import solve_it, Solver

class WebInterface():
    """
    Sedecordle web interface.  Save the driver value and go to the free
    web page
    """
    def __init__(self, website, delay):
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
        self.runs = 1
        self.clue_list = ["data", "not", "found"]

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
        for indx in range(16):
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
        if len(self.solver.winput) > 7:
            inm =  len(self.solver.winput) - 7
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

    def chk_word_in_grid(self, word):
        """
        Extract the color (Yellow/Green) information from words in the grid

        @param int word number of word to check
        @param int limitv maximum number of guesses made so far + 1
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
        sleep(self.delay)
        self.driver.get_screenshot_as_file(
            os.sep.join(["data", f"screenshot{score}.png"]))
        self.driver.quit()

if __name__ == "__main__":
    extract_data('answers')
    solve_it(WebInterface(WEBSITE, 10))
