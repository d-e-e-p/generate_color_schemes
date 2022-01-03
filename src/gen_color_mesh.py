#!/usr/bin/env python3
#
# generate objects containing colors within relative luminance limits
#

import colour
import progressbar

from colormath.color_diff import delta_e_cmc, delta_e_cie2000
from colormath.color_objects import LabColor, sRGBColor, HSVColor
from colormath.color_conversions import convert_color
from collections import defaultdict
import math

import meshio
import pymeshlab

import pudb
import sys

import numpy as np
import alphashape

from lib.ColorUtils import relative_lightness, lightness_hk

bar = progressbar.ProgressBar(maxval=100, \
    widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage(), ' ', progressbar.ETA()])



def gen_data_hsv_from_hsv(rl_limit_min, rl_limit_max):
    """
    main function
    """
    print(f" {rl_limit_min} < rl < {rl_limit_max}")
    scale = 25
    srgb1 = sRGBColor(0, 0, 0)
    srgb1_values = srgb1.get_value_tuple()
    lab1 = convert_color(srgb1, LabColor)
    pts = []
    step = 1
    for hsv_h in range(0,360,step):
        percent_complete = 100 * hsv_h/360
        bar.update(percent_complete)
        for hsv_v in np.arange(0, 1.01, 0.05):
            for hsv_s in np.arange(0, 1.01, 0.05):
                hsv2 = HSVColor(hsv_h, hsv_s, hsv_v)
                srgb2 = convert_color(hsv2, sRGBColor)
                srgb2_values = srgb2.get_value_tuple()
                rl =  relative_lightness(srgb1_values, srgb2_values)
                #print(f"{srgb2.get_rgb_hex()} : {luminous_from_Luv_plus_nayatani(srgb2_values)} {luminance_basic(srgb2_values)} rl={rl}")
                if rl > rl_limit_min and rl < rl_limit_max:
                    # radius_factor decreases with value hsv_v as it goes from 1 on top to 0
                    r = hsv_s * hsv_v
                    a = hsv_h * math.pi / 180
                    x,y = pol2cart(r,a)
                    z = hsv_v
                    pts.append([x,y,z])
                    test_hsv_to_rgb(hsv2, [x,y,z])
                    #print(f"{rgb_r} {rgb_g} {rgb_b} rl={int(rl)}")

    bar.finish()

    points = np.array(pts)
    return points


def gen_data_hsv_from_rgb(rl_limit_min, rl_limit_max):
    """
    main function
    """
    print(f" {rl_limit_min} < rl < {rl_limit_max}")
    scale = 25
    srgb1 = sRGBColor(0, 0, 0)
    srgb1_values = srgb1.get_value_tuple()
    lab1 = convert_color(srgb1, LabColor)
    pts = []
    step = 10
    for rgb_r in range(0,256,step):
        percent_complete = 100 * rgb_r/255
        bar.update(percent_complete)
        for rgb_g in range(0,256,step):
            for rgb_b in range(0,256,step):
                srgb2 = sRGBColor(rgb_r/255.,rgb_g/255., rgb_b/255.)
                srgb2_values = srgb2.get_value_tuple()
                rl =  relative_lightness(srgb1_values, srgb2_values)
                #print(f"{srgb2.get_rgb_hex()} : {luminous_from_Luv_plus_nayatani(srgb2_values)} {luminance_basic(srgb2_values)} rl={rl}")
                if rl > rl_limit_min and rl < rl_limit_max:
                    hsv = convert_color(srgb2, HSVColor)
                    r = hsv.hsv_s
                    a = hsv.hsv_h * math.pi / 180
                    x,y = pol2cart(r,a)
                    z = hsv.hsv_v
                    pts.append([x,y,z])
                    #print(f"{rgb_r} {rgb_g} {rgb_b} rl={int(rl)}")
                else:  
                    print(f"FOIOIIO rl = {rl}")

    bar.finish()

    points = np.array(pts)
    return points

# from https://stackoverflow.com/questions/20924085/python-conversion-between-coordinates
def cart2pol(x, y):
    rho = np.sqrt(x**2 + y**2)
    phi = np.arctan2(y, x)
    return(rho, phi)

def pol2cart(rho, phi):
    x = rho * np.cos(phi)
    y = rho * np.sin(phi)
    return(x, y)

def xyz_point_to_hsv_color(pt):
    x, y, z = pt
    r,a = cart2pol(x,y)
    hsv_h = a * 180 / math.pi
    if hsv_h < 0:
        hsv_h += 360
    if z != 0:
        hsv_s = r / z
    else:
        hsv_s = 0

    hsv_v = z
    hsv = HSVColor(hsv_h, hsv_s, hsv_v)
    return hsv

# TODO: vectorize this see https://stackoverflow.com/questions/35215161/most-efficient-way-to-map-function-over-numpy-array
def hsv_coords_to_rgb_colors(points):

    colors = []
    for pt in points:
        hsv = xyz_point_to_hsv_color(pt)
        srgb = convert_color(hsv, sRGBColor)
        colors.append([srgb.rgb_r, srgb.rgb_g, srgb.rgb_b])

    return np.array(colors)



def test_hsv_to_rgb(ohsv, pt):

    nhsv = xyz_point_to_hsv_color(pt)

    #print(f" H mismatch between o:{round(ohsv.hsv_h)} n:{round(nhsv.hsv_h)} diff:{round(ohsv.hsv_h-nhsv.hsv_h)}")
    if not math.isclose(ohsv.hsv_h , nhsv.hsv_h) and nhsv.hsv_s>0:
        print(f" H mismatch between o:{round(ohsv.hsv_h)} n:{round(nhsv.hsv_h)} diff:{round(ohsv.hsv_h-nhsv.hsv_h)} nhsv.hsv_s={nhsv.hsv_s}")
    if not math.isclose(ohsv.hsv_s , nhsv.hsv_s) and nhsv.hsv_v>0:
        print(f" S mismatch between o:{ohsv.hsv_s} n:{nhsv.hsv_s}")
    if not math.isclose(ohsv.hsv_v , nhsv.hsv_v) and nhsv.hsv_s>0:
        print(f" V mismatch between o:{ohsv.hsv_v} n:{nhsv.hsv_v}")

    srgb = convert_color(nhsv, sRGBColor)
    rgbhex =  srgb.get_rgb_hex()
    

    if len(rgbhex) != 7:
        print(f"pt={pt} ohsv={ohsv} new={nhsv} -> {srgb} -> {rgbhex}")

def gen_data_rgb_from_rgb(rl_limit_min, rl_limit_max):
    """
    main function
    """
    print(f" {rl_limit_min} < rl < {rl_limit_max}")
    scale = 25
    srgb1 = sRGBColor(0, 0, 0)
    srgb1_values = srgb1.get_value_tuple()
    lab1 = convert_color(srgb1, LabColor)
    pts = []
    step = 10
    for rgb_r in range(0,256,step):
        percent_complete = 100 * rgb_r/255
        bar.update(percent_complete)
        for rgb_g in range(0,256,step):
            for rgb_b in range(0,256,step):
                srgb2 = sRGBColor(rgb_r/255.,rgb_g/255., rgb_b/255.)
                srgb2_values = srgb2.get_value_tuple()
                rl =  relative_lightness(srgb1_values, srgb2_values)
                #print(f"{srgb2.get_rgb_hex()} : {lightness_hk(srgb1_values)} {lightness_hk(srgb2_values)} rl={rl}")
                #print(f"{srgb2.get_rgb_hex()} : {luminous_from_Luv_plus_nayatani(srgb2_values)} {luminance_basic(srgb2_values)} rl={rl}")
                if rl > rl_limit_min and rl < rl_limit_max:
                    x = rgb_r/255.
                    y = rgb_g/255.
                    z = rgb_b/255.
                    pts.append([x,y,z])
                    #print(f"{rgb_r} {rgb_g} {rgb_b} rl={int(rl)}")
    bar.finish()

    points = np.array(pts)
    return points

def add_and_save_mesh(step, tag, m, ms):
    tagstep = f"{tag}_{step}"
    ms.add_mesh(m, tagstep)
    filename = f"data/data_{tagstep}.ply"
    ms.save_current_mesh(filename)
    print(f"{step:10s} : saved {m.vertex_number():5d} vertex and {m.face_number():5d} faces to {filename}")

def create_mesh(points, mode, rl_limit_min, rl_limit_max,):

    tag = f"{mode}_{rl_limit_min}_to_{rl_limit_max}"
    print(f" creating mesh for {tag} with {len(points)} points")
    if len(points)  < 100:
        print(f" .. skipping too few points")
        return

    ms = pymeshlab.MeshSet()

    # save initial pointcloud with no faces
    step = "pre"
    faces = np.array([], dtype=np.int32).reshape(0,3)
    m = pymeshlab.Mesh( vertex_matrix=points, face_matrix=faces)
    add_and_save_mesh(step, tag, m, ms)

    # alpha: create a wrapper around pointcloud. 
    # somehow meshlab version doesn't work as well as alphashape.alphashape
    step = "alpha"
    alpha = 5
    hull = alphashape.alphashape(points, alpha)

    # load into meshlab to simplify by 50%
    m = pymeshlab.Mesh(hull.vertices, hull.faces)
    add_and_save_mesh(step, tag, m, ms)

    # filter: simplify and smooth
    # get defaults by:
    #default_params = ms.filter_parameter_values('meshing_decimation_quadric_edge_collapse')
    #default_params = ms.filter_parameter_values('apply_coord_laplacian_smoothing')
    step = "simplify"
    m = ms.current_mesh()
    #ms.meshing_decimation_quadric_edge_collapse(targetfacenum=2000)
    ms.meshing_decimation_quadric_edge_collapse(targetperc=0.5)
    ms.apply_coord_laplacian_smoothing(stepsmoothnum=5)
    add_and_save_mesh(step, tag, m, ms)

    # color verts based on coord
    step = "color"
    verts = m.vertex_matrix()
    faces = m.face_matrix()
    if mode == "rgb":
        colors = verts
    else:
        colors = hsv_coords_to_rgb_colors(verts)

    N = m.vertex_number()
    vert_colors = np.ones((N,4))
    vert_colors[:,:-1] = colors

    m = pymeshlab.Mesh( vertex_matrix=verts, face_matrix=faces, v_color_matrix=vert_colors)

    add_and_save_mesh(step, tag, m, ms)

    # very simple for display only
    step = "web"
    m = ms.current_mesh()
    ms.meshing_decimation_quadric_edge_collapse(targetperc=0.1)
    add_and_save_mesh(step, tag, m, ms)



    """
    #faces = np.empty(shape=[0, 3], dtype=np.int32)
    #verts = points
    ms.generate_alpha_shape(alpha=pymeshlab.Percentage(5), filtering=0)
    ms.generate_surface_reconstruction_ball_pivoting()
    ms.compute_texcoord_parametrization_triangle_trivial_per_wedge(textdim=1024)
    
    #meshio.write_points_cells(filename, points, [])
    #print(f"written pre mesh to {filename}")

    #ms = pymeshlab.MeshSet()
    #ms.load_new_mesh(filename)
    #print(len(ms))
    #print(ms.current_mesh().vertex_number())
    #m = ms.current_mesh()
    #v_matrix = m.vertex_matrix()
    #f_matrix = m.face_matrix()

    """


def gen_data(mode, rl_limit_min, rl_limit_max):
    """
    support different mesh geoms
    """
    if mode == "hsv":
        return gen_data_hsv_from_hsv(rl_limit_min, rl_limit_max)
    elif mode == "rgb":
        return gen_data_rgb_from_rgb(rl_limit_min, rl_limit_max)
    elif mode == "hsv_from_rgb":
        return gen_data_hsv_from_rgb(rl_limit_min, rl_limit_max)
    else:
        print(f"ERROR")
        sys.exit(-1)



if __name__ == "__main__":

    rl_max = 21

    limitpairs = [[0,25], [5,10]]
    limitpairs = [[0,5], [5,10], [10,15], [15,21]]

    mode = "rgb"
    for rl_limit_min,rl_limit_max in limitpairs:
        points = gen_data(mode, rl_limit_min, rl_limit_max)
        create_mesh(points, mode, rl_limit_min, rl_limit_max)


    mode = "hsv"
    for rl_limit_min,rl_limit_max in limitpairs:
        points = gen_data(mode, rl_limit_min, rl_limit_max)
        create_mesh(points, mode, rl_limit_min, rl_limit_max)


