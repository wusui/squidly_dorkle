# (c) 2022 Warren Usui
# Squidly_dorkle
# This code is licensed under the MIT license (see LICENSE.txt for details)
"""
Squidly_dorkle
"""
from web_interface import WebInterface
from web_interface import WEBSITE
from random_backend import RandomBackend
from file_io import extract_data
from brainz import solve_it

SIMULATE = False
WEBRUN = True

def squidly_dorkle():
    """
    First run the simulator 1000 times to exercise brainz.
    Then run the it once against the web-site
    """
    extract_data('allowed')
    extract_data('answers')
    if SIMULATE:
        sim_numb = 1000
        for _ in range(sim_numb):
            solve_it(RandomBackend())
        RandomBackend.show_stats(RandomBackend(), sim_numb)
    if WEBRUN:
        solve_it(WebInterface(WEBSITE, 10))

if __name__ == "__main__":
    squidly_dorkle()
