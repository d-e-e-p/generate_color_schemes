"""
class that deals with color convertion and measurement routines
"""

import pudb
from colormath.color_diff import delta_e_cmc, delta_e_cie2000
from colormath.color_objects import LabColor, sRGBColor, HSVColor
from colormath.color_conversions import convert_color

# TODO: switch from colormath to colour
import colour
from colour.appearance import XYZ_to_Nayatani95
from colour.plotting import colour_style, plot_multi_colour_swatches
from colour.utilities import message_box
from colour.notation.hexadecimal import (
    RGB_to_HEX,
    HEX_to_RGB,
)


import math

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import pandas as pd

from pathlib import Path

from lib.SAPC_0_98G_4g_minimal import SAPC_0_98G_4g_minimal

import pudb


class ColorUtils:
    def __init__(self):
        self.average_luminance = 0.14
        self.L_a = 250 * self.average_luminance
        self.wp = colour.xy_to_Luv_uv([0.31271, 0.32902])

    def vac_luminous_from_hk_effect(self, xyz):
        Luv = colour.XYZ_to_Luv(xyz)
        uv  = colour.Luv_to_uv(Luv)
        VAC = colour.HelmholtzKohlrausch_effect_luminous_Nayatani1997( uv, self.wp, self.L_a, method='VAC')
        return VAC

    def vac_object_from_hk_effect(self, xyz):
        """
            XYZ_to_Nayatani95(XYZ, XYZ_n, Y_o, E_o, E_or, n=1):

        Parameters
        ----------
        XYZ :
        XYZ_n : *CIE XYZ* tristimulus values of reference white.
        Y_o : Luminance factor :math:`Y_o` of achromatic background as percentage
            normalised to domain [0.18, 1.0] in **'Reference'** domain-range scale.
        E_o : Illuminance :math:`E_o` of the viewing field in lux.
        E_or : Normalising illuminance :math:`E_{or}` in lux usually normalised to
            domain [1000, 3000].
        n : Noise term used in the non-linear chromatic adaptation model.
        """
        Luv = colour.XYZ_to_Luv(xyz)
        uv  = colour.Luv_to_uv(Luv)
        VAC = colour.HelmholtzKohlrausch_effect_object_Nayatani1997( uv, self.wp, self.L_a, method='VAC')
        return VAC

    def lightness_hk_xyz(self, xyz):
        lab = colour.XYZ_to_Lab(xyz)
        lstar = lab[0]
        if lstar == 0:
            VAC = 0
        else:
            VAC = self.vac_object_from_hk_effect(xyz)
        lightness = lstar * VAC
        return lightness

    def lightness_hk_rgb(self, rgb):
        xyz = colour.sRGB_to_XYZ(rgb)
        return self.lightness_hk_xyz(xyz)


    def luminance_basic(self, cin):
        """
        assume cin in RGB order
        formula from http://www.brucelindbloom.com/index.html?Eqn_RGB_to_XYZ.html
         Y is luminance
         L is lightness
        """

        cout = []
        for ci in cin:
            if ci <= 0.04045:
                co = ci/12.92
            else:
                co = ((ci+0.055)/1.055) ** 2.4
            cout.append(co)

        sRco = 0.2126729
        sGco = 0.7151522
        sBco = 0.0721750
        Y = sRco * cout[0] + sGco * cout[1] + sBco * cout[2]
        return Y

    def lightness_basic(self, cin):
        """
        assume cin in RGB order
        formula from http://www.brucelindbloom.com/index.html?LContinuity.html
         Y is luminance
         L is lightness
        """
        Y = self.luminance_basic(cin)
        κ = 24389 / 27.
        ϵ = 216 / 24389.
        if Y <= ϵ:
            L = κ * Y
        else:
            L = 116 * Y ** (1/3.) - 16

        return L

    def contrast_ratio_APCA(self, cfg, cbg):
        # see https://stackoverflow.com/questions/56198778/what-is-the-efficient-way-to-calculate-human-eye-contrast-difference-for-rgb-val
        Yfg = self.luminance_basic(cfg)
        Ybg = self.luminance_basic(cbg)
        return SAPC_0_98G_4g_minimal.APCAcontrast(Yfg,Ybg)

    def contrast_diff_lstar(self, cfg, cbg):
        return self.lightness_hk_rgb(cfg) -  self.lightness_hk_rgb(cbg)


    @staticmethod
    def rgb_to_hex(colors_rgb):
        colors_rgbhex = []
        for color in colors_rgb:
            rgb = sRGBColor(*color)
            hex = rgb.get_rgb_hex()
            colors_rgbhex.append(hex)
        return colors_rgbhex
 
    @staticmethod
    def delta_e_rgb(c1,c2):
        srgb1 =  sRGBColor(*c1)
        srgb2 =  sRGBColor(*c2)
        lab1 = convert_color(srgb1, LabColor)
        lab2 = convert_color(srgb2, LabColor)
        delta = delta_e_cie2000(lab1,lab2)
        return delta

    @staticmethod
    def convert_color_rgbhex_to_lab(color):
        """
        convert color from rgbhex to lab
        """
        r = int(color[1:3], 16) / 255.0
        g = int(color[3:5], 16) / 255.0
        b = int(color[5:7], 16) / 255.0

        c =  sRGBColor(r, g, b)
        lab = convert_color(c, LabColor)
        return lab

    def delta_e_rgbhex(self, color1, color2):
        delta = delta_e_cie2000(self.convert_color_rgbhex_to_lab(color1), self.convert_color_rgbhex_to_lab(color2))
        return delta


    def print_delta_e_hsv_stats(self, n_samples, colors_hsv):

        colors_rgbhex = []
        for color in colors_hsv:
            hsv =  HSVColor(*color)
            rgb =  convert_color(hsv, sRGBColor)
            hex = rgb.get_rgb_hex()
            colors_rgbhex.append(hex)

        min_delta = math.inf
        for c1 in colors_rgbhex:
            print(f"{c1} : ",end='')
            for c2 in colors_rgbhex:
                delta = self.delta_e_rgbhex(c1,c2)
                print(f"{delta:3.0f} ", end='')
                if c1 != c2:
                    if delta < min_delta:
                        min_delta = delta
            print("")
        print("")
        print(f"with n={n_samples} min delta = {min_delta}")


    def print_delta_e_rgb_stats(self, n_samples, colors_rgb):

        colors_rgbhex = rgb_to_hex(colors_rgb)

        min_delta = math.inf
        for c1 in colors_rgbhex:
            print(f"{c1} : ",end='')
            for c2 in colors_rgbhex:
                delta = self.delta_e_rgbhex(c1,c2)
                print(f"{delta:3.0f} ", end='')
                if c1 != c2:
                    if delta < min_delta:
                        min_delta = delta
            print("")
        print("")
        ret = f"with n={n_samples} min deltaE = {round(min_delta)}"
        print(ret)
        return round(min_delta)


    def saveplot_delta_e_rgb_stats(self, tag, n_samples, colors_rgb, min_delta_e):

        dir = f"res/images_{tag}"
        Path(dir).mkdir(parents=True, exist_ok=True)

        colors_rgbhex = self.rgb_to_hex(colors_rgb)
        plt.style.use(['dark_background'])

        # multiple line plots
        for hex in colors_rgbhex:
            label = f" {hex}"
            df=pd.DataFrame({'x_values': range(1,11), label: np.random.randn(10)})
            line, = plt.plot( 'x_values', label, data=df, marker='o', markerfacecolor=hex, markersize=12, color=hex, linewidth=4)


        # show legend
        comment = f"with n={n_samples} min deltaE = {round(min_delta_e)}"
        plt.title(comment)
        #plt.legend(loc='right')
        plt.legend(loc=7)
        #plt.savefig(f"res/img{n_samples}.png", facecolor=fig.get_facecolor(), transparent=True)
        plt.savefig(f"{dir}/img{n_samples}.png")

        plt.close()



