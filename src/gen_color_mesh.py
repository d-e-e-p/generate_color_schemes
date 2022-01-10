#!/usr/bin/env python3
#
# generate objects containing colors within relative luminance limits
#

import colour
import progressbar

from colormath.color_diff import delta_e_cmc, delta_e_cie2000
from colormath.color_objects import LabColor, sRGBColor, HSVColor, HSLColor
from colormath.color_conversions import convert_color
from collections import defaultdict
import math

import meshio
import pymeshlab

import pudb
import sys

import numpy as np
import pandas as pd

import alphashape
from scipy.spatial import ConvexHull

from lib.ColorUtils import ColorUtils
from lib.colorconversion_js import colorconversion_js
# use for okhsl_to_srgb, srgb_to_okhsl


# from https://stackoverflow.com/questions/2600790/multiple-levels-of-collection-defaultdict-in-python
class DeepDict(defaultdict):
    def __call__(self):
        return DeepDict(self.default_factory)


# globals
c = ColorUtils()
bar = progressbar.ProgressBar(maxval=100, \
    widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage(), ' ', progressbar.ETA()])


def print_delta_stats(items):
    df_describe = pd.DataFrame(items)
    print(df_describe.describe())


def gen_lightness_matrix(mode):
    if mode == 'rgb':   
        return rgb_to_lightness_matrix()
    elif mode == 'hsv':
        return hsv_to_lightness_matrix()
    elif mode == 'okhsl':
        return hsl_to_lightness_matrix(type="ok")
    elif mode == 'hsl':
        return hsl_to_lightness_matrix(type="normal")
    else:
        print("ERROR")
        sys.exit(-1)

def rgb_to_lightness_matrix():

    m =  DeepDict(DeepDict(DeepDict(int)))
    print(f"creating rgb_to_lightness_matrix")

    scale = 25
    srgb1 = sRGBColor(0, 0, 0)
    srgb1_values = srgb1.get_value_tuple()
    pts = []
    deltas = []
    step = 10
    bar.start()
    for rgb_r in range(0,256,step):
        percent_complete = 100 * rgb_r/255
        bar.update(percent_complete)
        for rgb_g in range(0,256,step):
            for rgb_b in range(0,256,step):
                srgb2 = sRGBColor(rgb_r/255.,rgb_g/255., rgb_b/255.)
                srgb2_values = srgb2.get_value_tuple()
                dl =  c.delta_lightness(srgb2_values, srgb1_values)
                m[rgb_r][rgb_g][rgb_b] = dl
                deltas.append(dl)

    bar.finish()
    print_delta_stats(deltas)
    return m

def hsl_to_lightness_matrix(type="ok"):

    m =  DeepDict(DeepDict(DeepDict(int)))
    print(f"creating {type}hsl_to_lightness_matrix")
    deltas = []
    scale = 25
    srgb1 = sRGBColor(0, 0, 0)
    srgb1_values = srgb1.get_value_tuple()
    lab1 = convert_color(srgb1, LabColor)
    step = 10
    bar.start()
    for hsl_h in range(0,360,step):
        percent_complete = 100 * hsl_h/360
        bar.update(percent_complete)
        for hsl_s in np.arange(0, 1.01, 0.05):
            for hsl_l in np.arange(0, 1.01, 0.05):
                if type == "ok":
                    okhsl_h = hsl_h / 360 # <--- important correction for okhsl
                    sr,sg,sb = colorconversion_js.okhsl_to_srgb(okhsl_h, hsl_s, hsl_l)
                    srgb2 = sRGBColor(sr/255., sg/255.,sb/255.)
                else:
                    hsl   = HSLColor(hsl_h, hsl_s, hsl_l)
                    srgb2 = convert_color(hsl, sRGBColor)

                srgb2_values = srgb2.get_value_tuple()
                dl =  c.delta_lightness(srgb2_values, srgb1_values)
                m[hsl_h][hsl_s][hsl_l] = dl
                deltas.append(dl)
    bar.finish()
    print_delta_stats(deltas)
    return m

def hsv_to_lightness_matrix():

    m =  DeepDict(DeepDict(DeepDict(int)))
    print(f"creating hsv_to_lightness_matrix")
    deltas = []
    scale = 25
    srgb1 = sRGBColor(0, 0, 0)
    srgb1_values = srgb1.get_value_tuple()
    lab1 = convert_color(srgb1, LabColor)
    step = 1
    bar.start()
    for hsv_h in range(0,360,step):
        percent_complete = 100 * hsv_h/360
        bar.update(percent_complete)
        for hsv_v in np.arange(0, 1.01, 0.05):
            for hsv_s in np.arange(0, 1.01, 0.05):
                hsv2 = HSVColor(hsv_h, hsv_s, hsv_v)
                srgb2 = convert_color(hsv2, sRGBColor)
                srgb2_values = srgb2.get_value_tuple()
                dl =  c.delta_lightness(srgb2_values, srgb1_values)
                m[hsv_h][hsv_v][hsv_s] = dl
                deltas.append(dl)
    bar.finish()
    print_delta_stats(deltas)
    return m

def gen_data_hsl_from_hsl(m, dl_min, dl_max):
    """
    main function
    """
    zscale = 2.0
    print(f" {dl_min} < rl < {dl_max}")
    pts = []
    for hsl_h,sdict in m.items(): 
        for hsl_s,ldict in sdict.items():
            for hsl_l,delta_lightness in ldict.items():
                #print(f"{srgb2.get_rgb_hex()} : {luminous_from_Luv_plus_nayatani(srgb2_values)} {luminance_basic(srgb2_values)} rl={rl}")
                if delta_lightness >= dl_min and  delta_lightness <= dl_max:
                    # radius_factor decreases with value hsl_v as it goes from 0.5 to (0,1)
                    if hsl_l < 0.5:
                        factor = 2 * hsl_l
                    else:
                        factor = 2 * (1 - hsl_l)
                    #print(f"factor {hsl_l} {factor}")
                    r = hsl_s * factor
                    a = hsl_h * math.pi / 180
                    x,y = pol2cart(r,a)
                    z = hsl_l * zscale
                    pts.append([x,y,z])
                    #test_hsl_to_rgb([hsl_h, hsl_s, hsl_v], [x,y,z])
                    #print(f"{rgb_r} {rgb_g} {rgb_b} rl={int(rl)}")

    bar.finish()

    points = np.array(pts)
    return points

def gen_data_hsv_from_hsv(m, dl_min, dl_max):
    """
    main function
    """
    print(f" {dl_min} < rl < {dl_max}")
    pts = []
    for hsv_h,vdict in m.items(): 
        for hsv_v,sdict in vdict.items():
            for hsv_s,delta_lightness in sdict.items():
                #print(f"{srgb2.get_rgb_hex()} : {luminous_from_Luv_plus_nayatani(srgb2_values)} {luminance_basic(srgb2_values)} rl={rl}")
                if delta_lightness >= dl_min and  delta_lightness <= dl_max:
                    # radius_factor decreases with value hsv_v as it goes from 1 on top to 0
                    r = hsv_s * hsv_v
                    a = hsv_h * math.pi / 180
                    x,y = pol2cart(r,a)
                    z = hsv_v
                    pts.append([x,y,z])
                    test_hsv_to_rgb([hsv_h, hsv_s, hsv_v], [x,y,z])
                    #print(f"{rgb_r} {rgb_g} {rgb_b} rl={int(rl)}")

    bar.finish()

    points = np.array(pts)
    return points

def gen_data_rgb_from_rgb(m, dl_min, dl_max):
    """
    main function
    """
    print(f" {dl_min} < rl < {dl_max}")
    pts = []
    for rgb_r,gdict in m.items(): 
        for rgb_g,bdict in gdict.items():
            for rgb_b,delta_lightness in bdict.items():
                #print(f"{srgb2.get_rgb_hex()} : {lightness_hk(srgb1_values)} {lightness_hk(srgb2_values)} rl={rl}")
                #print(f"{srgb2.get_rgb_hex()} : {luminous_from_Luv_plus_nayatani(srgb2_values)} {luminance_basic(srgb2_values)} rl={rl}")
                if delta_lightness >= dl_min and  delta_lightness <= dl_max:
                    x = rgb_r/255.
                    y = rgb_g/255.
                    z = rgb_b/255.
                    pts.append([x,y,z])
                    #print(f"{rgb_r} {rgb_g} {rgb_b} rl={int(rl)}")

    points = np.array(pts)
    return points

def gen_data_hsv_from_rgb(m, dl_min, dl_max):
    """
    main function
    """
    print(f" {dl_min} < rl < {dl_max}")
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
                delta_lightness =  c.delta_lightness(srgb2_values, srgb1_values)
                #print(f"{srgb2.get_rgb_hex()} : {luminous_from_Luv_plus_nayatani(srgb2_values)} {luminance_basic(srgb2_values)} rl={rl}")
                if  delta_lightness >= dl_min and delta_lightness <= dl_max:
                    hsv = convert_color(srgb2, HSVColor)
                    r = hsv.hsv_s
                    a = hsv.hsv_h * math.pi / 180
                    x,y = pol2cart(r,a)
                    z = hsv.hsv_v
                    pts.append([x,y,z])
                    #print(f"{rgb_r} {rgb_g} {rgb_b} rl={int(rl)}")
                else:  
                    print(f"not in range rl = {rl}")

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

def xyz_coord_to_hsl_color(pt):
    """
    reverse pol to cart
    """
    zscale = 2.0
    x, y, z = pt
    r,a = cart2pol(x,y)
    hsl_h = a * 180 / math.pi
    if hsl_h < 0:
        hsl_h += 360
    hsl_l = z / zscale

    # ok, now the complicated piece because of weird shape
    #   if x < 0.5 y=2x
    #   if x > 0.5 y=2(1-x)
    # to reverse:
    #   if x < 0.5 y=1/(2x)
    #   if x > 0.5 y=1/((2(1-x))
    if hsl_l < 0.5:
        factor = 2 * hsl_l
    else:
        factor = 2 * (1 - hsl_l)
    if factor != 0:
        hsl_s = r / factor
    else:
        hsl_s = 0
    return [hsl_h, hsl_s, hsl_l]

def xyz_coord_to_hsv_color(pt):
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
        hsv = xyz_coord_to_hsv_color(pt)
        srgb = convert_color(hsv, sRGBColor)
        colors.append([srgb.rgb_r, srgb.rgb_g, srgb.rgb_b])

    return np.array(colors)

def okhsl_coords_to_rgb_colors(points):

    colors = []
    for pt in points:
        hsl_h, hsl_s, hsl_l = xyz_coord_to_hsl_color(pt)
        hsl_h /= 360 # <--- important correction for okhsl
        srgb_r, srgb_g, srgb_b = colorconversion_js.okhsl_to_srgb(hsl_h, hsl_s, hsl_l)
        colors.append([srgb_r/255., srgb_g/255, srgb_b/255.])
        hsl = HSLColor(hsl_h, hsl_s, hsl_l)
        srgb = convert_color(hsl, sRGBColor)
        okhsl = colorconversion_js.srgb_to_okhsl(255*srgb.rgb_r,255*srgb.rgb_g,255*srgb.rgb_b)
        #if hsl.hsl_h != 0:
        #    print(f" hsl:{hsl} [{255*srgb.rgb_r:.0f}, {255*srgb.rgb_g:.0f}, {255*srgb.rgb_b:.0f}] vs [{srgb_r:.0f},{srgb_g:.0f},{srgb_b:.0f}] expect h ratio={okhsl[0] / hsl.hsl_h:.2f}")

        

    return np.array(colors)

def hsl_coords_to_rgb_colors(points):

    colors = []
    for pt in points:
        hsl_h, hsl_s, hsl_l = xyz_coord_to_hsl_color(pt)
        hsl = HSLColor(hsl_h, hsl_s, hsl_l)
        srgb = convert_color(hsl, sRGBColor)
        colors.append([srgb.rgb_r, srgb.rgb_g, srgb.rgb_b])

    return np.array(colors)



def test_hsv_to_rgb(hsv_pt, xyz_pt):

    ohsv = HSVColor(*hsv_pt)
    nhsv = xyz_coord_to_hsv_color(xyz_pt)

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
        print(f"ERROR pt={pt} ohsv={ohsv} new={nhsv} -> {srgb} -> {rgbhex}")


def add_and_save_mesh(step, tag, ms, m=None):
    if m is None:
        m = ms.current_mesh()
    tagstep = f"{tag}_{step}"
    ms.add_mesh(m, tagstep)
    filename = f"data/data_{tagstep}.ply"
    ms.save_current_mesh(filename)
    out_dict = ms.get_geometric_measures()
    bbox = out_dict['bbox']
    dim = f"[{bbox.dim_x():.1f},{bbox.dim_y():.1f},{bbox.dim_z():.1f}]"
    print(f"{step:10s} : saved {ms.current_mesh().vertex_number():5d} vertex and {m.face_number():5d} faces of {dim} to {filename} ")

def create_mesh(points, mode, dl_min, dl_max,):

    tag = f"{mode}_{dl_min}_to_{dl_max}"
    print(f" creating mesh for {tag} with {len(points)} points")
    if len(points)  < 100:
        print(f" .. skipping too few points")
        return

    ms = pymeshlab.MeshSet()
    ms.set_verbosity(False)

    # save initial pointcloud with no faces
    step = "pre"
    faces = np.array([], dtype=np.int32).reshape(0,3)
    m = pymeshlab.Mesh( vertex_matrix=points, face_matrix=faces)
    add_and_save_mesh(step, tag, ms, m=m)

    # alpha: create a wrapper around pointcloud. 
    # somehow meshlab version doesn't work as well as alphashape.alphashape
    step = "alpha"
    alpha = 5

    # rgb shapes have concave faces
    if mode == 'rgb':
        hull = alphashape.alphashape(points, alpha)
        vertices = hull.vertices
        faces = hull.faces
    else:
        hull = ConvexHull(points, qhull_options='Q12')
        vertices = hull.points
        faces = hull.simplices
        
    # load into meshlab to simplify by 50%
    m = pymeshlab.Mesh(vertices, faces)
    add_and_save_mesh(step, tag, ms, m)

    # filter: simplify and smooth
    # get defaults by:
    #default_params = ms.filter_parameter_values('meshing_decimation_quadric_edge_collapse')
    #default_params = ms.filter_parameter_values('apply_coord_laplacian_smoothing')
    step = "simplify"
    m = ms.current_mesh()
    #ms.meshing_decimation_quadric_edge_collapse(targetfacenum=2000)
    ms.meshing_remove_unreferenced_vertices()
    add_and_save_mesh("unref", tag, ms)
    if mode == "okhsl" or mode == "hsl":
        v_count_before = ms.current_mesh().vertex_number()
        # history: smoothflag=False is definately needed
        #{'iterations': 3, 'adaptive': True, 'selectedonly': False, 'targetlen': 0.03464101627469063, 'featuredeg': 30.0, 'checksurfdist': False,
        #'maxsurfdist': 0.03464101627469063, 'splitflag': True, 'collapseflag': False, 'swapflag': True, 'smoothflag': False, 'reprojectflag': True}
        ms.meshing_isotropic_explicit_remeshing(iterations=3, adaptive=False, collapseflag=False, smoothflag=False)
        v_count_after  = ms.current_mesh().vertex_number()
        #print(f"meshing_isotropic_explicit_remeshing increased v from {v_count_before} to {v_count_after}")
    else:
        ms.meshing_decimation_quadric_edge_collapse(targetperc=0.5)
        ms.apply_coord_laplacian_smoothing(stepsmoothnum=5)

    add_and_save_mesh(step, tag, ms)
    #pu.db

    # color verts based on coord
    step = "color"
    m = ms.current_mesh()
    verts = m.vertex_matrix()
    faces = m.face_matrix()
    if mode == "rgb":
        colors = verts
    elif mode == "hsv":
        colors = hsv_coords_to_rgb_colors(verts)
    elif mode == "okhsl":
        colors = okhsl_coords_to_rgb_colors(verts)
    elif mode == "hsl":
        colors = hsl_coords_to_rgb_colors(verts)
    else:
        print(f"unknown mode = {mode}")

    N = m.vertex_number()
    vert_colors = np.ones((N,4))
    vert_colors[:,:-1] = colors

    m = pymeshlab.Mesh( vertex_matrix=verts, face_matrix=faces, v_color_matrix=vert_colors)
    add_and_save_mesh(step, tag,  ms, m)

    # very simple for display only
    step = "web"
    ms.meshing_decimation_quadric_edge_collapse(targetperc=0.1)
    add_and_save_mesh(step, tag, ms)



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


def gen_data(mode, m, dl_min, dl_max):
    """
    support different mesh geoms
    """
    if mode == "hsv":
        return gen_data_hsv_from_hsv(m, dl_min, dl_max)
    elif mode == "rgb":
        return gen_data_rgb_from_rgb(m, dl_min, dl_max)
    elif mode == "hsv_from_rgb":
        return gen_data_hsv_from_rgb(m, dl_min, dl_max)
    elif mode == "okhsl" or mode == "hsl":
        return gen_data_hsl_from_hsl(m, dl_min, dl_max)
    else:
        print(f"ERROR")
        sys.exit(-1)


def get_limitpairs(starts,widths,bloat=0):
    """
    return list that looks like:

        limitpairs = [[0,25], [5,10]]
        limitpairs = [[0,5], [5,10], [10,15], [15,21]]
        limitpairs = [[0,25], [25,50], [50,75], [75,100]]

    """

    limitpairs = []
    i = 0
    max = 12
    for st in starts:
        for wd in widths:
            end = st + wd
            if end > max or wd == 0:
                continue
            i += 1
            st_limit = st*10 - bloat
            end_limit = end*10 + bloat
            print(f"iteration {i} s {st_limit} end {end_limit}")
            limitpairs.append([st_limit,end_limit])

    print(f"{limitpairs}")
    return limitpairs

if __name__ == "__main__":

    #starts = range(4,10)
    #widths = range(1,10)

    starts = [0]
    widths = range(12)
    bloat  = 0
    limitpairs = get_limitpairs(starts,widths,bloat)
    #sys.exit()

    #for mode in ['rgb','hsv']:
    for mode in ['okhsl']:
        m = gen_lightness_matrix(mode)
        for dl_min,dl_max in limitpairs:
            points = gen_data(mode, m, dl_min, dl_max)
            create_mesh(points, mode, dl_min, dl_max)




