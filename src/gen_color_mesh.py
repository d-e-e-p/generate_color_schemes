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

import numpy as np
import alphashape

bar = progressbar.ProgressBar(maxval=100, \
    widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage(), ' ', progressbar.ETA()])

def relative_luminance(color1, color2, method='basic'):
    if method == 'basic':
        l1 = (luminance_basic(color1) + 0.05)
        l2 = (luminance_basic(color2) + 0.05)
    else:
        l1 = (luminous_from_Luv_plus_nayatani(color1) + 0.05)
        l2 = (luminous_from_Luv_plus_nayatani(color2) + 0.05)
    if l1 > l2:
        rl = l1/l2
    else:
        rl = l2/l1
    if method == 'basic':
        return rl
    else:
        return rl / 100

# measures of relative brighness
def luminous_from_Luv_plus_nayatani(sRGB):
    # Adapting Luminance, 250 cd/m^2 represents a typical modern computer display peak luminance.
    # need to assume average_luminance of final image
    if sRGB == (0,0,0):
        sRGB = (1e-10,1e-10,1e-10)

    average_luminance = 0.14
    L_a = 250 * average_luminance
    wp = colour.xy_to_Luv_uv([0.31271, 0.32902])
    xyz = colour.sRGB_to_XYZ(sRGB)
    luv = colour.XYZ_to_Luv(xyz)
    uv  = colour.Luv_to_uv(luv)
    VCC = colour.HelmholtzKohlrausch_effect_luminous_Nayatani1997(
        uv, wp, L_a, method='VCC')
    lstar = luv[0]
    luminous_factor = lstar * VCC
    return luminous_factor

def luminance_basic(cin):
    """
    assume RGB order
    """
    cout = []
    for ci in cin:
        if ci <= 0.03928:
            co = ci/12.92
        else:
            co = ((ci+0.055)/1.055) ** 2.4
        cout.append(co)

    L = 0.2126 * cout[0] + 0.7152 * cout[1] + 0.0722 * cout[2]
    return L

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
                rl =  relative_luminance(srgb1_values, srgb2_values, method='basic')
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
                rl =  relative_luminance(srgb1_values, srgb2_values, method='basic')
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
    steptag = f"{step}_{tag}"
    ms.add_mesh(m, steptag)
    filename = f"data/data_{steptag}.ply"
    ms.save_current_mesh(filename)
    print(f"{step:10s} : saved {m.vertex_number():5d} vertex and {m.face_number():5d} faces to {filename}")

def create_mesh(points, rl_limit_min, rl_limit_max):

    tag = f"rgb_{rl_limit_min}_to_{rl_limit_max}"
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
    ms.meshing_decimation_quadric_edge_collapse(targetperc=0.5)
    ms.apply_coord_laplacian_smoothing(stepsmoothnum=5)
    add_and_save_mesh(step, tag, m, ms)

    # color verts based on coord
    step = "color"
    verts = m.vertex_matrix()
    faces = m.face_matrix()
    N = m.vertex_number()
    vert_colors = np.ones((N,4))
    vert_colors[:,:-1] = verts

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




if __name__ == "__main__":

    rl_max = 20

    for limit in  range(5,16,1):
        for width in range(5,40,5):
            rl_limit_min = limit 
            rl_limit_max = limit + width
            if rl_limit_max > 20:
                continue
            print(f"{rl_limit_min} -> {rl_limit_max}")

            points = gen_data_rgb_from_rgb(rl_limit_min, rl_limit_max)
            create_mesh(points, rl_limit_min, rl_limit_max)




