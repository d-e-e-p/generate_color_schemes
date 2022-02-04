#!/usr/bin/env python3
"""
    result swatches

"""

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from glob import glob
import re
import math
from json_tricks import loads
from pathlib import Path

from lib.ColorUtils import ColorUtils
c = ColorUtils()


def read_json_file(filename):
    print(f"read {filename}")
    with open(filename,"r+") as f:
        json = f.read()
    items = loads(json)
    return items


def write_html_file(dir,html, tag, n, sortby):
    filename = f"{dir}/{sortby}/res_lightness_{tag}_n{n}.html"
    fp = open(filename , 'w')
    fp.write(html)
    fp.close()
    print(f"written {filename}")

def sort_by_lightness(colors):

    color_list = []
    for col in colors:
        lightness = c.lightness_hk_rgbhex(col)
        color_list.append([lightness,col])

    return sorted(color_list)

def sort_by_hue(colors):

    color_list = []
    for col in colors:
        hsl = c.convert_color_rgbhex_to_hsl(col)
        hue = hsl.hsl_h
        color_list.append([hue,col])

    return sorted(color_list)

def sort_by_saturation(colors):

    color_list = []
    for col in colors:
        hsl = c.convert_color_rgbhex_to_hsl(col)
        saturation = hsl.hsl_s
        color_list.append([saturation,col])

    return sorted(color_list)

def sort_colorlist(sortby, colors):
    """
    use globals to find sort function
    works but maybe should use a dict instead?
    """
    func = f"sort_by_{sortby}"
    return globals()[func](colors)

def get_fg_from_color(color):
    """
    super simplistic version for now 
    TODO: refine selection
    """
    lightness = c.lightness_hk_rgbhex(color)
    if lightness > 50:
        return "black"
    else:
        return "white"

def calc_tile_width(n):
    """
        100% = full width
    """
    border_padding   = 3
    min_width        = 8
    min_line_padding = 3   # for stuff
    min_width        = 11  # includes 2 for border on each side and 1 for padding
    max_width        = 43  # half the page

    min_total_width = n * min_width - min_line_padding
    cmt = f"debug: min_total_width = {min_total_width} \n"
    if min_total_width < 100:
        width = (100  - min_line_padding) / float(n)
        if width > max_width:
            tile_width = (max_width - border_padding)
        else:
            tile_width = (width - border_padding)
        cmt += f"single line, width = {width} so tile_width={tile_width}"
    else:
        num_lines = math.ceil(min_total_width / 100)
        target_total_width = num_lines * 100
        padding_corr = num_lines * min_line_padding
        # distribute over lines
        width = (target_total_width - padding_corr)  / float(n)
        tile_width = (width - border_padding)
        cmt += f"n={n} num_lines={num_lines} target_total_width={target_total_width} width = ({target_total_width} - {padding_corr})/{n} = {width:.2f} so tile_width={width:.2f} - {border_padding} = {tile_width:.2f}"

    tile_width = float(f"{tile_width:.2f}")
    cmt += f"n={n} tile_width={tile_width}"
    return tile_width, cmt

def get_selected_option(sortby):
    sel_L, sel_H, sel_S = "", "", ""

    selected = ' selected="selected" '

    if   (sortby == "lightness" ): sel_L = selected
    elif (sortby == "hue"       ): sel_H = selected
    elif (sortby == "saturation"): sel_S = selected
    else:
        print("ERROR in sortby = {sortby}")
        sys.exit(-1)
    return sel_L, sel_H, sel_S


def generate_table_header(tag, n, sortby):
    #print(f"running tag {tag} for {n} ")


    # calculate width per tile
    #tile_width, comment = calc_tile_width(n)


    html = """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
</head>
<body>
    <div class=everything>
        <div class=label_and_box>
  """

    match = re.search(r"(\d+)_to_(\d+)", tag)
    if match:
        tag_from = match[1]
        tag_to   = match[2]
    else:
        print(f"tag={tag} not matched pattern")
        sys.exit(-1)


    # add selected="selected" based on sortby
    sel_l, sel_h, sel_s = get_selected_option(sortby)

    h3 = f"""
Palette for
<label for="num_colors">N=<label>
<select  id="num_colors" onChange="update_num_colors(this.options[this.selectedIndex].value)">
"""

    for i in range(26):
        if i == n:
            sel = ' selected="selected"'
        else:
            sel = ''
        h3 += f"""<option {sel} value="{i}">{i}</option>"""

    h3 += f"""
</select> Colors
<label for="sortby">( Sorted by <label>
<select  id="sortby" onChange="update_sortby(this.options[this.selectedIndex].value)">
  <option {sel_l} value="lightness">lightness</option>
  <option {sel_h} value="hue">hue</option>
  <option {sel_s} value="saturation">saturation</option>
</select> )"""
    html += f"""
            <h3>{h3}</h3>
            <div class="wrapper">
            """

    return html


def generate_table_sortby_saturation(colors, color2name):

    saturation_color_list = sort_by_saturation(colors)
    #print(f"{saturation_color_list}")


    html = ""

    for saturation,color in saturation_color_list:
        name = color2name.get(color, "placeholder for now")
        fg = get_fg_from_color(color)
        style = f"background-color:{color};color:{fg}"
        #html += """<label for="favcolor">"""
        html += f'<div class="box" style="{style}"><sup>S={saturation:.1f}</sup><br>{color}<br><sub>{name}</sub></div>\n'
        #html += f"""</label><input type="color" id="favcolor" name="favcolor" value="{color}">"""

    html += f"""
            </div>
           </div>
        <br>
         <div class=label_and_box>
          <h1>colored text on background</h1>
          <div class="wrapper" title="text on background test">
          """

    for saturation,color in saturation_color_list:
        name = color2name.get(color, "placeholder for now")
        fg = get_fg_from_color(color)
        style = f"color:{color}; border-color:{color};"
        html += f'<div class="box" style="{style}"><sup>S={saturation:.1f}</sup><br>{color}<br><sub>{name}</sub></div>\n'

    return html

def generate_table_sortby_hue(colors, color2name):

    hue_color_list = sort_by_hue(colors)
    #print(f"{hue_color_list}")


    html = ""

    for hue,color in hue_color_list:
        name = color2name.get(color, "placeholder for now")
        fg = get_fg_from_color(color)
        style = f"background-color:{color};color:{fg}"
        #html += """<label for="favcolor">"""
        html += f'<div class="box" style="{style}"><sup>H={hue:.0f}°</sup><br>{color}<br><sub>{name}</sub></div>\n'
        #html += f"""</label><input type="color" id="favcolor" name="favcolor" value="{color}">"""

    html += f"""
            </div>
           </div>
        <br>
         <div class=label_and_box>
          <h1>colored text on background</h1>
          <div class="wrapper" title="text on background test">
          """

    for hue,color in hue_color_list:
        name = color2name.get(color, "placeholder for now")
        fg = get_fg_from_color(color)
        style = f"color:{color}; border-color:{color};"
        html += f'<div class="box" style="{style}"><sup>H={hue:.0f}</sup><br>{color}<br><sub>{name}</sub></div>\n'

    return html

def generate_table_sortby_lightness(colors, color2name):

    lightness_color_list = sort_by_lightness(colors)
    #print(f"{lightness_color_list}")


    html = ""

    for lightness,color in lightness_color_list:
        name = color2name.get(color, "placeholder for now")
        fg = get_fg_from_color(color)
        style = f"background-color:{color};color:{fg}"
        #html += """<label for="favcolor">"""
        html += f'<div class="box" style="{style}"><sup>L={lightness:.0f}</sup><br>{color}<br><sub>{name}</sub></div>\n'
        #html += f"""</label><input type="color" id="favcolor" name="favcolor" value="{color}">"""

    html += f"""
            </div>
           </div>
        <br>
         <div class=label_and_box>
          <h1>colored text on background</h1>
          <div class="wrapper" title="text on background test">
          """

    for lightness,color in lightness_color_list:
        name = color2name.get(color, "placeholder for now")
        fg = get_fg_from_color(color)
        style = f"color:{color}; border-color:{color}; "
        html += f'<div class="box" style="{style}"><sup>L={lightness:.0f}</sup><br>{color}<br><sub>{name}</sub></div>\n'

    return html

def get_value_str(sortby,value):
    if   (sortby == "lightness" ): str = f"L={value:.0f}"
    elif (sortby == "hue"       ): str = f"H={value:.0f}°"
    elif (sortby == "saturation"): str = f"S={value:.2f}"
    else:
        print("ERROR in sortby = {sortby}")
        sys.exit(-1)
    return str



def generate_table_body(sortby, colors, color2name):


    value_color_list = sort_colorlist(sortby, colors)


    html = ""

    for value,color in value_color_list:
        colorname = color2name.get(color, "placeholder for now")
        fg = get_fg_from_color(color)
        style = f"background-color:{color};color:{fg}"
        sup = get_value_str(sortby,value)
        #html += """<label for="favcolor">"""
        html += f'<div class="box" style="{style}"><sup>{sup}</sup><br>{color}<br><sub>{colorname}</sub></div>\n'
        #html += f"""</label><input type="color" id="favcolor" name="favcolor" value="{color}">"""

    html += f"""
            </div>
           </div>
        <br>
         <div class=label_and_box>
          <h1>colored text on background</h1>
          <div class="wrapper" title="text on background test">
          """

    for value,color in value_color_list:
        name = color2name.get(color, "placeholder for now")
        fg = get_fg_from_color(color)
        style = f"color:{color}; border-color:{color}; "
        sup = get_value_str(sortby,value)
        html += f'<div class="box" style="{style}"><sup>{sup}</sup><br>{color}<br><sub>{name}</sub></div>\n'

    return html


def generate_table_footer(tag, sortby, n ):
    dir = "/assets/res/html/json"
    url_json = f"{dir}/dark/{sortby}/res_lightness_{tag}.html"

    dir = "/assets/res/html/json"
    url = f"{dir}/{sortby}/res_lightness_{tag}.html"

    results_file = f"res_lightness_{tag}_n{n}.html"

    html = f"""
           </div>
    </div>

    </div>

</body>
</html>
    """
    return html

def generate_table(tag, colors, n, sortby,  color2name):
    #print(f"running tag {tag} for {n} ")

    # instead of if then else tree
    generate_table_by_sort = {}
    generate_table_by_sort["lightness"]  = generate_table_sortby_lightness
    generate_table_by_sort["hue"]        = generate_table_sortby_hue
    generate_table_by_sort["saturation"] = generate_table_sortby_saturation


    # ok gen html in 3 steps
    html = generate_table_header(tag, n, sortby)
    #html += generate_table_by_sort[sortby](colors, color2name)
    html += generate_table_body(sortby, colors, color2name)
    html += generate_table_footer(tag, sortby, n)

    return html



def main():

    dir = "res/html/swatch"
    sortby_list =  "saturation hue lightness".split()
    max_n = 25

    # make dirs upfront
    for sortby in sortby_list:
        Path(f"{dir}/{sortby}").mkdir(parents=True, exist_ok=True)

    # name info
    json_file = "res/json/color2name.json"
    color2name = read_json_file(json_file)
    print(f"color2name = {color2name}")

    # read in   res/rgb_50_to_75_color_list.json
    # read and  res/rgb_50_to_70_delta_e_list.json
    pattern1 = "res/json/rgb_*_color_list.json"
    pattern2 = "res/json/rgb_*_delta_list.json"

    json_files = sorted(glob(pattern1))
    for file in json_files:
        items = read_json_file(file)
        match = re.search(r"_(\d+_to_\d+)_", file)
        if match:
            tag = match[1]
            for n in range(1,max_n + 1):
                colors = items[str(n)]
                for sortby in sortby_list:
                    html = generate_table(tag,colors, n, sortby, color2name )
                    write_html_file(dir,html, tag, n, sortby)


if __name__ == '__main__':

    main()


