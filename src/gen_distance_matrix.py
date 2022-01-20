#!/usr/bin/env python3
"""

gen_distance_matrix.py 

    read in coordinates in ply file and 

"""


from glob import glob

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

import meshio
import progressbar
import re

import numpy as np

from lib.ColorUtils import ColorUtils

# globals
c = ColorUtils()
bar = progressbar.ProgressBar(maxval=100, \
    widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage(), ' ', progressbar.ETA()])


def save_distance_rgb(pts, tag, metric):

    distance_matrix = []
    num_pts = len(pts)
    idx = 0
    bar.start()
    for c1 in pts:
        line = []
        for c2 in pts:
            distance = c.delta_rgb(c1,c2,metric)
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


def get_ply_files():
    data_dir = "data/"
    ply_files = []
    for datafile in sorted(glob(os.path.join(data_dir, '*rgb*' + "_color.ply"))):
        match = re.search(r"_(\d+_to_\d+)_color.ply", datafile)
        if match:
            tag = match[1]
            ply_files.append([tag,datafile])
    print(f"ply_files: {ply_files}")
    return ply_files


if __name__ == "__main__":
    metric = 'delta_e2000'
    metric = 'hyab'
    ply_files = get_ply_files()
    #ply_files = [['60_to_80', 'data/data_rgb_60_to_80_color.ply']]
    for tag,datafile in ply_files:
        print(f"loading {datafile}")
        hull = meshio.read(datafile)
        save_distance_rgb(hull.points, tag, metric)


