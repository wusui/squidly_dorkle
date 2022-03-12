# (c) 2022 Warren Usui
# Squidly_dorkle
# This code is licensed under the MIT license (see LICENSE.txt for details)
"""
Squidly_dorkle real program
"""
from random_backend import RandomBackend
from brainz import solve_it
if __name__ == "__main__":
    solve_it(RandomBackend(1000))
