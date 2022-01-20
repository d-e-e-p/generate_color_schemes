#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Helmholtz—Kohlrausch effect comparison 
Variable Achromatic Color (VAC) 
from https://github.com/colour-science/colour/blob/develop/colour/examples/appearance/examples_hke.py
"""

import sys
import os
import colour
from colour.plotting import colour_style, plot_multi_colour_swatches
from colour.utilities import message_box
from colour.notation.hexadecimal import (
    RGB_to_HEX,
)
import numpy as np
import math

# Js2Py of https://github.com/Myndex/SAPC-APCA/blob/master/JS/SAPC_0_98G_4g_minimal.js
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from lib.ColorUtils import ColorUtils



def lightness_camhunt(xyz):
    CCT_w = 6504
    camH = colour.XYZ_to_Hunt(xyz, bg_grey, bg_grey, L_a, XYZ_p=bg_grey,CCT_w=CCT_w, S=0.14,S_w=0.14)
    return camH.J

def lightness_camzcam(xyz):
    Y_b = 20.0
    camZ = colour.XYZ_to_ZCAM(xyz, wp_grey,L_a,Y_b)
    return camZ.J


# from https://stackoverflow.com/questions/736043/checking-if-a-string-can-be-converted-to-float-in-python
def is_float(element):
    try:
        float(element)
        return True
    except ValueError:
        return False

def compare_contrast_ratios(xyz):

    lstardelta = c.delta_lightness(xyz, bg_grey)

    cr_APCA = c.contrast_ratio_APCA(
            colour.XYZ_to_sRGB(xyz),
            colour.XYZ_to_sRGB(bg_grey))

    srgb = colour.XYZ_to_sRGB(xyz)
    hex = RGB_to_HEX(srgb)

    return [hex, lstardelta, cr_APCA]

def compare_luminosity(xyz):
    Y_o = 20.0
    E_o = 5000.0
    E_or = 1000.0

    lab = colour.XYZ_to_Lab(xyz)
    lstar = lab[0]
    srgb = colour.XYZ_to_sRGB(xyz)
    hex = RGB_to_HEX(srgb)
    VAC = c.vac_object_from_hk_effect(xyz)

    #L∗NVAC = L∗+[−0.1340 q(q)+0.0872 KBr] suv L∗

    surround = colour.VIEWING_CONDITIONS_CAM16['Average']
    Y_b = 20.0
    CCT_w = 6504
    camH = colour.XYZ_to_Hunt(xyz, bg_grey, bg_grey, L_a, XYZ_p=bg_grey,CCT_w=CCT_w, S=0.14,S_w=0.14)
    #camL = colour.XYZ_to_LLAB(xyz, bg_grey, Y_b, L_a)
    camK = colour.XYZ_to_Kim2009(xyz, bg_grey,L_a)
    camZ = colour.XYZ_to_ZCAM(xyz, wp_grey,L_a,Y_b)
    litB = c.lightness_basic(srgb)
    #cam = XYZ_to_Nayatani95(xyz, bg_grey, Y_o, E_o, E_or)
    #print(f"{hex} Lbasic:{litB:.0f} L*:{lstar:.0f}  VAC:{VAC:.2f} L∗NVAC  :{round(lstar*VAC)} camH:{camH.J:.0f} camK:{camK.J:.0f} camZ:{camZ.J:.0f} ")
    #print(f"{hex} {litB:.0f} {lstar:.0f} {VAC:.2f} {round(lstar*VAC)} {camH.J:.0f} {camK.J:.0f} {camZ.J:.0f} ")
    return [hex, litB , lstar , lstar*VAC, camH.J , camZ.J]

def gen_old_patches():

    swatches_uv = [
        [0.45079660, 0.52288689],
        [0.19124902, 0.55444488],
        [0.13128455, 0.51210591],
        [0.14889223, 0.37091478],
        [0.28992574, 0.30964533],
    ]
    swatches_XYZ_old = []
    #swatches_XYZ_old.append(colour.sRGB_to_XYZ(np.array([1,1,1])))
    for patch in swatches_uv:
        in_XYZ = colour.Luv_to_XYZ((colour.uv_to_Luv(patch)))
        swatches_XYZ_old.append(in_XYZ * (average_luminance / in_XYZ[1]))

    swatches_XYZ_old.append(bg_grey)
    return swatches_XYZ_old

def gen_new_patches(swatches_XYZ_old, metric='L*VAC'):
    """
    colors match the l*VAC instead or l*
    """
    targets = {}
    steps = {}
    abs_tols = {}
    functions = {}
    targets['L*VAC'] = 47
    steps['L*VAC'] = 0.0001
    abs_tols['L*VAC'] = 0.01
    functions['L*VAC'] = c.lightness_hk_xyz

    targets['camHunt'] = 225
    steps['camHunt'] = 0.0001
    abs_tols['camHunt'] = 0.1
    functions['camHunt'] = lightness_camhunt

    targets['camZCAM'] = 24
    steps['camZCAM'] = 0.0001
    abs_tols['camZCAM'] = 0.01
    functions['camZCAM'] = lightness_camzcam

    # step1: find multiplier m
    m = np.ones(len(swatches_XYZ_old))
    target = targets[metric]
    step = steps[metric]
    function = functions[metric]
    abs_tol = abs_tols[metric]
    for i in range(len(swatches_XYZ_old)):
        patch = swatches_XYZ_old[i] 
        VAC =  c.vac_luminous_from_hk_effect(patch)
        m[i] = VAC
        lightness = function(patch)
        print(f"initial {i} {patch} {lightness}")
        while not math.isclose(lightness, target, abs_tol=abs_tol):
            if lightness < target:
                m[i] -= step
            else:
                m[i] += step
            lightness = function(patch / m[i])
            #print(f"{i} {metric} : m {m[i]} {lightness} {target} diff={lightness-target}")

    # step2: compare VAC
    for i in range(len(swatches_XYZ_old)):
        patch = swatches_XYZ_old[i] 
        VAC = c.vac_luminous_from_hk_effect(patch)
        print(f" {i} VAC:{VAC:.2f} m:{m[i]:.2f}")

    # step3: create new patches
    swatches_XYZ_new = []
    for i in range(len(m)):
        patch = swatches_XYZ_old[i] / m[i]
        swatches_XYZ_new.append(patch)

    #swatches_XYZ_old.append(bg_grey)
    #swatches_XYZ_new.append(bg_grey)
    return swatches_XYZ_new


def dump_res_table(res):
    for line in res:
        for item in line:
            if is_float(item):
                print(f"{float(item):5.0f}  ", end='')
            else:
                print(f"{item:10}  ", end='')
        print()
    print()
    return res
    #sys.exit()

def dump_results_spreadsheet(swatches_XYZ):

    res = []
    res.append("hex litB  L*  L*VAC camHunt camZCAM".split())
    for patch in swatches_XYZ:
        line = compare_luminosity(patch)
        res.append(line)
    dump_res_table(res)

    res = []
    res.append("hex L*D SAPC".split())
    for patch in swatches_XYZ:
        line = compare_contrast_ratios(patch)
        res.append(line)
    dump_res_table(res)



def save_plot(*patches):

    columns = len(patches)
    num_patches = len(patches[0])

    swatches_plot = []
    for i in range(num_patches):
        for patch in patches:
            swatches_plot.append(colour.XYZ_to_sRGB(bg_grey))
            swatches_plot.append(colour.XYZ_to_sRGB(patch[i]))
            print(f"{i} : {patch[i]}")


    colour_style()
    message_box(f"Plotting swatches {patches}")
    #fig1,_ = plot_multi_colour_swatches(swatches_plot, compare_swatches='stacked')
    fig1,_ = plot_multi_colour_swatches(swatches_plot, compare_swatches='stacked', columns=columns )
    fig1.savefig(f"patch_compare{num_patches}.png")

#
# body 
#



average_luminance = 0.14
L_a = 250 * average_luminance
wp = colour.xy_to_Luv_uv([0.31271, 0.32902])
contrast_ratio_target = 5
bg_grey = colour.xy_to_XYZ(colour.Luv_uv_to_xy(wp)) * average_luminance / contrast_ratio_target
wp_grey = colour.xy_to_XYZ(colour.Luv_uv_to_xy(wp)) * average_luminance * 10

c = ColorUtils()

if __name__ == "__main__":


    swatches_XYZ_old = gen_old_patches()
    dump_results_spreadsheet(swatches_XYZ_old)


    swatches_XYZ_new1 = gen_new_patches(swatches_XYZ_old)
    dump_results_spreadsheet(swatches_XYZ_new1)
    #swatches_XYZ_old.append(colour.sRGB_to_XYZ(np.array([0,0,0])))
    sys.exit()

    save_plot(swatches_XYZ_old, swatches_XYZ_new1)



    swatches_XYZ_new2 = gen_new_patches(swatches_XYZ_old, 'camHunt')
    dump_results_spreadsheet(swatches_XYZ_new2)

    swatches_XYZ_new3 = gen_new_patches(swatches_XYZ_old, 'camZCAM')
    dump_results_spreadsheet(swatches_XYZ_new3)

    save_plot(swatches_XYZ_old, swatches_XYZ_new1, swatches_XYZ_new2, swatches_XYZ_new3)



