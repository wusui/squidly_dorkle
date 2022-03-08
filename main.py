# (c) 2022 Warren Usui
# Squidy_dorkle
# This code is licensed under the MIT license (see LICENSE.txt for details)
"""
Squidy_dorkle
"""
from web_interface import WebInterface
from web_interface import WEBSITE
from brainz import solve_it
if __name__ == "__main__":
    solve_it(WebInterface(WEBSITE, 10))
