# (c) 2022 Warren Usui
# Squidly_dorkle
# This code is licensed under the MIT license (see LICENSE.txt for details)
"""
Interface to the sedecordle webpage
"""
import os

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import chromedriver_autoinstaller

WEBSITE = "http://sedecordle.com"

class WebInterface():
    """
    Sedecordle web interface.  Save the driver value and go to the free
    web page
    """
    def __init__(self, website, delay):
        chromedriver_autoinstaller.install()
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.driver = webdriver.Chrome(service=Service(), options=options)
        self.driver.get(website)
        self.driver.maximize_window()
        elem1 = self.driver.find_element(By.ID, "free")
        elem1.click()
        self.delay = delay
        self.max_times = 1

    def add_word(self, word):
        """
        Add a word into the sedecordle grid.  Sends character by character
        data and saves the word in self.input

        @param word String word that is being guessed
        """
        for letter in word:
            elem = self.driver.find_element(By.ID, letter)
            elem.click()
        elem = self.driver.find_element(By.ID, "enter2")
        elem.click()

    def identify_if_solved(self):
        """
        Look at the background color of the final page.  Solved if green,
        failed if red.
        """
        elem1 = self.driver.find_element(By.ID, "body")
        bgc_info = elem1.value_of_css_property("background-color")
        header = "unsolved"
        if bgc_info.find("0, 128, 0,") > 0:
            header = "solved"
        return header

    def chk_word_in_grid(self, word, limitv):
        """
        Extract the color (Yellow/Green) information from words in the grid

        @param String word word to check
        @param int limitv Length of word (default 5)
        """
        indx = []
        for guess in range(1, limitv):
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

    def multi_record(self, count):
        """
        Stub when using web interface
        """
        print(self.delay)
        print("Should not get here: " + str(count))

    def shutdown(self):
        """
        Save a screen shot and exit
        """
        self.driver.get_screenshot_as_file(
            os.sep.join(["data", "screenshot.png"]))
        self.driver.quit()
