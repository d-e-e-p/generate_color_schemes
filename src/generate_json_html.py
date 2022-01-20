#!/usr/bin/env python3
"""
    farthest-point-sampling

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


def write_html_file(dir, html, tag, theme, sortby):
    filename = f"{dir}/{theme}/{sortby}/res_lightness_{tag}.html"
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

def get_values_with_attr(values, sortby, color2name):

    values_with_attr = []
    for color in values:
        name = color2name.get(color, "placeholder for now")
        name = f'"{name}"'
        lightness = c.lightness_hk_rgbhex(color)
        hsl = c.convert_color_rgbhex_to_hsl(color)
        hue = hsl.hsl_h
        saturation = hsl.hsl_s
        values_with_attr.append([color,lightness,hue,saturation,name])

    order_of_values_with_attr = {'lightness': 1, 'hue': 2, 'saturation': 3}
    order = order_of_values_with_attr[sortby] 
    values_with_attr = sorted(values_with_attr, key=lambda x: x[order])
    return values_with_attr



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
        cmt += "single line, width = {width} so tile_width={tile_width}"
    else:
        num_lines = math.ceil(min_total_width / 100)
        target_total_width = num_lines * 100
        padding_corr = num_lines * min_line_padding
        # distribute over lines
        width = (target_total_width - padding_corr)  / float(n)
        tile_width = (width - border_padding)
        cmt += f"n={n} num_lines={num_lines} target_total_width={target_total_width} width = ({target_total_width} - {padding_corr})/{n} = {width} so tile_width={width} - {border_padding} = {tile_width}"

    tile_width = float(f"{tile_width:.2f}")
    cmt += f"n={n} tile_width={tile_width}"
    return tile_width, cmt

def generate_table_header(tag, theme, sortby):
    #print(f"running tag {tag} for {n} {theme}")

    if theme == "dark":
        fgcolor = "white"
        bgcolor = "black"
    else:
        fgcolor = "black"
        bgcolor = "white"
  
    # calculate width per tile

    html = """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta charset="utf-8" />
 <style type="text/css">
html { 
    width: 100vw; font-family: monospace; color: """ +  fgcolor + """; background-color: """ + bgcolor + """ ; margin: 1%;
}
h1 { 
    font-size: 3vw; float: none; text-align: center; margin: 1%; 
}
h2 { 
    font-size: 2vw; float: none; text-align: center; margin: 1%; 
}

body {
    margin: 0;
}

/* see https://stackoverflow.com/questions/18634213/adding-scissor-with-dotted-line-at-the-bottom-of-the-page */
#scissors {
    height: 43px; /* image height */
    width: 90%;
    margin: auto auto;
    background-image: url('http://i.stack.imgur.com/cXciH.png');
    background-repeat: no-repeat;
    background-position: right;
    position: relative;
    overflow: hidden;
}
#scissors:after {
    content: "";
    position: relative;
    top: 50%;
    display: block;
    border-top: 3px dashed black;
    margin-top: -3px;
}

/* see https://stackoverflow.com/questions/33790275/center-pre-block-without-centering-text */
.container {
   text-align: center;
 }

.container pre {
  display: inline-block;
  text-align: left;
 }

/* see https://stackoverflow.com/questions/826782/how-to-disable-text-selection-highlighting */
.noselect {
  -webkit-touch-callout: none; /* iOS Safari */
    -webkit-user-select: none; /* Safari */
     -khtml-user-select: none; /* Konqueror HTML */
       -moz-user-select: none; /* Old versions of Firefox */
        -ms-user-select: none; /* Internet Explorer/Edge */
            user-select: none; /* Non-prefixed version, currently
                                  supported by Chrome, Edge, Opera and Firefox */
}

 </style>
</head>
<body>

  """

    match = re.search(r"(\d+)_to_(\d+)", tag)
    if match:
        tag_from = match[1]
        tag_to   = match[2]
    else:
        print(f"tag={tag} not matched pattern")
        sys.exit(-1)

    title = f"colors of lightness from {tag_from} to {tag_to}" 
    html += f"""

<h1 class="noselect">{title}</h1>
<h2 class="noselect">num_colors: [rgbhex, lightness, hue, saturation, name]</h2>
<h2 class="noselect">Usage: select-all, copy, paste a valid json file</h2>

<div id="scissors"></div>
<div class="container">
            """

    return html




def generate_table_body(sortby, items, color2name):


    html = "<br><pre>\n"
    html += "{\n";
    index1 = 0
    num_values1 = len(items.keys())
    for key, values in items.items():
        html += f'\t"{key}": [\n'
        index2 = 0
        num_values2 = len(values)

        values_with_attr = get_values_with_attr(values, sortby, color2name)

        for color,lightness,hue,saturation,name in values_with_attr:

            html += f'\t\t["{color}", {lightness:5.0f}, {hue:5.0f}, {saturation:5.2f}, {name:>25}]' 
            index2 += 1
            if (index2 != num_values2):
                html += ", "
            else:
                html += "  "
            html += f'<em style="background-color: {color};">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</em>\n' 
        index1 += 1
        if (index1 != num_values1):
            html += "\t],\n"
        else:
            html += "\t]\n"

    html += "}\n"
    html += "</pre>\n"
    return html

def generate_table_footer():
    html = f"""
</div>
<div id="scissors"></div>
</body>
</html>
    """
    return html

def generate_table(tag, theme, sortby, items, color2name ):
    #print(f"running tag {tag} for {n} {theme}")


    # ok gen html in 3 steps
    html = generate_table_header(tag, theme, sortby)
    html += generate_table_body(sortby, items, color2name)
    html += generate_table_footer()

    return html



def main():

    dir = "res/html/json"
    themes =  "dark light".split()
    sortby_list =  "lightness hue saturation".split()

    # make dirs upfront
    for theme in themes:
        for sortby in sortby_list:
            Path(f"{dir}/{theme}/{sortby}").mkdir(parents=True, exist_ok=True)

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
            for theme in themes:
                for sortby in sortby_list:
                    html = generate_table(tag, theme, sortby, items, color2name )
                    write_html_file(dir, html, tag, theme, sortby)


if __name__ == '__main__':

    main()


