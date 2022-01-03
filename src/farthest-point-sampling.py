#!/usr/bin/env python3
"""
    farthest-point-sampling

"""

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
import logging
import colorama
from colorama import Fore, Back, Style
import pudb
import numpy as np
from glob import glob
import meshio
import re
import math
from json_tricks import dumps, loads
from pathlib import Path


from lib.ColorUtils import  print_delta_e_rgb_stats, saveplot_delta_e_rgb_stats, rgb_to_hex

from lib.fps_v2 import FPS

def load_distance_matrix_rgb(tag):
    filename = f"data/distance_matrix_{tag}.npy"
    with open(filename, 'rb') as f:
        distance_matrix = np.load(f)
    print(f"loaded distance_matrix {distance_matrix.shape} from {filename}")
    return distance_matrix

def write_json_file(filename, items):
    json = dumps(items, indent=4)
    fp = open(filename , 'w')
    fp.write(json)
    fp.close()
    print(f"written {filename}")

def run_fps(pts, tag):
    distance_matrix = load_distance_matrix_rgb(tag)

    color_list = {}
    delta_e_list = {}
    for n_samples in range(2,24):
        fps = FPS(pts, distance_matrix,  n_samples)
        print(f"Running FPS over {len(pts)} points and getting {n_samples} samples")
        selected_pts = fps.run()  # Get all samples.
        #print_delta_e_hsv_stats(n_samples,selected_pts)
        min_delta_e = print_delta_e_rgb_stats(n_samples,selected_pts)
        saveplot_delta_e_rgb_stats(tag, n_samples,selected_pts, min_delta_e)
        color_list[n_samples] = rgb_to_hex(selected_pts)
        delta_e_list[n_samples] = min_delta_e

    # save color_list and delta results
    file_color_list = f"res/rgb_{tag}_color_list.json"
    write_json_file(file_color_list, color_list)

    file_delta_e_list = f"res/rgb_{tag}_delta_e_list.json"
    write_json_file(file_color_list, delta_e_list)



if __name__ == '__main__':

    data_dir = "data/"
    for datafile in glob(os.path.join(data_dir, '*' + "_web.ply")):
            print(f"loading {datafile}")
            hull = meshio.read(datafile)
            match = re.search(r"_(\d+_to_\d+)_web.ply", datafile)
            if match:
                tag = match[1]
                run_fps(hull.points, tag)


