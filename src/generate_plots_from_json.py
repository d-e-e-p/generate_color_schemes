#!/usr/bin/env python3
"""
    generate_plots_from_json.py

"""

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from glob import glob
import re
import math
from json_tricks import loads
from pathlib import Path
import pudb

import progressbar

from lib.ColorUtils import ColorUtils
c = ColorUtils()

bar = progressbar.ProgressBar(maxval=100, \
    widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage(), ' ', progressbar.ETA()])


def read_json_file(filename):
    print(f"read {filename}")
    with open(filename,"r+") as f:
        json = f.read()
    items = loads(json)
    return items




def main():

    dir = "res/plots"
    themes =  "dark light".split()
    types  =  "delta examples".split()

    # make dirs upfront
    for type in types:
        for theme in themes:
            Path(f"{dir}/{type}/{theme}").mkdir(parents=True, exist_ok=True)

    # name info
    json_file = "res/json/color2name.json"
    color2name = read_json_file(json_file)
    #print(f"color2name = {color2name}")

    # read in   res/rgb_50_to_75_color_list.json
    # read and  res/rgb_50_to_70_delta_list.json
    pattern1 = "res/json/rgb_*_color_list.json"
    pattern2 = "res/json/rgb_*_delta_list.json"

    color_list = {}
    json_files = sorted(glob(pattern1))
    bar.start()
    i = 0
    n = len(json_files)
    for file1 in json_files:
        percent_complete = (100.0 * i)/n
        bar.update(percent_complete)
        i += 1
        items = read_json_file(file1)
        match = re.search(r"_(\d+_to_\d+)_", file1)
        if match:
            tag = match[1]
            file2 = f"res/json/rgb_{tag}_delta_list.json"
            min_delta_list = read_json_file(file2)
            for type in types:
                for theme in themes:
                    c.saveplot_delta_plot_alln(dir, type, tag, theme, items, min_delta_list)
    bar.finish()
       


if __name__ == '__main__':

    main()
    print("done")


