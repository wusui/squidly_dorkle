# (c) 2022 Warren Usui
# Squidly_dorkle
# This code is licensed under the MIT license (see LICENSE.txt for details)
"""
Squidly_dorkle real program
"""
from web_interface import WebInterface
from web_interface import WEBSITE
from file_io import extract_data
from brainz import solve_it
if __name__ == "__main__":
    extract_data('allowed')
    extract_data('answers')
    solve_it(WebInterface(WEBSITE, 10))
