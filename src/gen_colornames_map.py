#!/usr/bin/env python3
"""

src/gen_colornames_map.py 

    names for selected colors

"""


from glob import glob

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

import progressbar
import itertools
from json_tricks import dumps, loads


from colour.notation.hexadecimal import (
    HEX_to_RGB,
    )

from lib.ColorUtils import ColorUtils

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

def read_json_file(filename):
    print(f"read {filename}")
    with open(filename,"r+") as f:
        json = f.read()
    items = loads(json)
    return items

def write_json_file(filename, items):
    json = dumps(items, indent=4, allow_nan=True, conv_str_byte=True, ensure_ascii=False)
    fp = open(filename , 'w')
    fp.write(json)
    fp.close()
    print(f"written {filename}")

def read_json_color2names(filename):
    print(f"read {filename}")
    with open(filename,"r+") as f:
        json = f.read()
    items = loads(json)
    color2names = {}
    for item in items:
        color2names[item['hex']] = item['name']

    return color2names

def find_index_closest_color(target_hex, colors_rgb):
    metric = 'delta_e2000'
    c1 = HEX_to_RGB(target_hex)
    clist = []
    for c2 in colors_rgb:
        distance = c.delta_rgb(c1,c2,metric)
        clist.append([distance,c2])

    min_value = min(clist)
    min_index = clist.index(min_value)
    return min_index

# https://stackoverflow.com/questions/952914/how-to-make-a-flat-list-out-of-a-list-of-lists
def flatten(t):
    return [item for sublist in t for item in sublist]

def get_target_colors():
    target_colors = []
    pattern1 = "res/json/rgb_*_color_list.json"
    json_files = sorted(glob(pattern1))
    for file in json_files:
        items = read_json_file(file)
        target_colors.extend(list(itertools.chain(items.values())))

    # sort + uniq
    target_colors = flatten(target_colors)
    target_colors = sorted(set(target_colors))
    return target_colors

if __name__ == "__main__":
    json_file = "src/data/colornames.json"
    colors2names = read_json_color2names(json_file)
    colors_rgb = convert_hex_to_list(colors2names)

    target_colors = get_target_colors()
    print(f"{target_colors}")            

    color2name = {}
    bar = progressbar.ProgressBar(maxval=100, \
    widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage(), ' ', progressbar.ETA()])
    bar.start()
    i = 0
    n = len(target_colors)
    isave = 10
    filename = "res/json/color2name.json"
    for target_hex in target_colors:
        i += 1
        percent_complete = (100.0 * i)/n
        bar.update(percent_complete)
        closest_color_index = find_index_closest_color(target_hex, colors_rgb)
        matched_hex = list(colors2names.keys())[closest_color_index]
        matched_name = colors2names[matched_hex]
        color2name[target_hex] = matched_name
        if ( i % isave == 0 ):
            write_json_file(filename,color2name)

    bar.finish()
    write_json_file(filename,color2name)


"""

    target_hex = "#3d1c00"
    print(f"closest name for {target_hex} is {matched_name}")

"""


