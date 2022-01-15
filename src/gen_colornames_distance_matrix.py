#!/usr/bin/env python3
"""

gen_colornames_distance_matrix.py 

    read in coordinates in json colornames file

"""

import lib

from glob import glob

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
import logging
import colorama
from colorama import Fore, Back, Style

import meshio
import progressbar
import re
from json_tricks import dumps, loads

import numpy as np

from colour.notation.hexadecimal import (
    RGB_to_HEX,
    HEX_to_RGB,
    )

from lib.ColorUtils import ColorUtils
from gen_distance_matrix import save_distance_rgb

# globals
c = ColorUtils()
bar = progressbar.ProgressBar(maxval=100, \
    widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage(), ' ', progressbar.ETA()])



def convert_hex_to_list(colors2names):
    colors_hex = colors2names.keys()
    colors_rgb = []
    for hex in colors_hex:
        rgb = HEX_to_RGB(hex)
        colors_rgb.append(rgb)
    return colors_rgb


def read_json_color2names(filename):
    print(f"read {filename}")
    with open(filename,"r+") as f:
        json = f.read()
    items = loads(json)
    color2names = {}
    for item in items:
        color2names[item['hex']] = item['name']

    return color2names

if __name__ == "__main__":
    metric = 'delta_e2000'
    json_file = "src/data/colornames.json"
    colors2names = read_json_color2names(json_file)
    colors_rgb = convert_hex_to_list(colors2names)
    save_distance_rgb(colors_rgb,"colornames",metric)



