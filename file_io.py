# (c) 2022 Warren Usui
# Squidy_dorkle
# This code is licensed under the MIT license (see LICENSE.txt for details)
"""
Stuff that writes files in this directory goes here
"""
from os.path import exists
import requests

from web_interface import WEBSITE

def extract_data(field):
    """
    Write the allowed and answer files from data extracted from the
    sedecordle code

    @param field String file name (allowed or answers)
    """
    from_loc = ''.join([field, ' = "'])
    if exists(from_loc):
        return
    wpage = requests.get(WEBSITE)
    tfront = str(wpage.content)
    first_str = tfront[tfront.find(from_loc):]
    ret_data = first_str[0:first_str.find('".split(')]
    with open(''.join([field, ".txt"]), 'w', encoding="utf8") as fdesc:
        fdesc.write(ret_data[len(from_loc):])