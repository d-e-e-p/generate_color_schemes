#!/usr/bin/env python3
"""

gen_distance_matrix.py 

    read in coordinates in ply file and 

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

import numpy as np

from lib.ColorUtils import delta_e_rgb

bar = progressbar.ProgressBar(maxval=100, \
    widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage(), ' ', progressbar.ETA()])



def save_delta_e_rgb(pts, tag):

    distance_matrix = []
    num_pts = len(pts)
    idx = 0
    bar.start()
    for c1 in pts:
        line = []
        for c2 in pts:
            distance = delta_e_rgb(c1,c2)
            line.append(distance)
        percent_complete = 100 * idx/num_pts
        bar.update(percent_complete)
        idx += 1
        distance_matrix.append(line)

    bar.finish()
    print()
    distance_matrix = np.array(distance_matrix)
    filename = f"data/distance_matrix_{tag}.npy"
    with open(filename, 'wb') as f:
        np.save(f, distance_matrix)
    print(f"distance_matrix of {distance_matrix.shape} saved to {filename}")




if __name__ == "__main__":

    data_dir = "data/"
    for datafile in glob(os.path.join(data_dir, '*' + "_web.ply")):
            print(f"loading {datafile}")
            hull = meshio.read(datafile)
            match = re.search(r"_(\d+_to_\d+)_web.ply", datafile)
            if match:
                tag = match[1]
                save_delta_e_rgb(hull.points, tag)


