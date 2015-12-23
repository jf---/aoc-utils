#!/usr/bin/python
# coding: utf-8

r"""display/color.py
"""

from __future__ import division

import OCC.Quantity


def color(r, g, b):
    r"""Create a OCC.Quantity.Quantity_Color from RGB components

    Parameters
    ----------
    r : float
        Red component between 0 and 1
    g : float
        Green component between 0 and 1
    b : blue
        Blue component between 0 and 1

    Returns
    -------
    OCC.Quantity.Quantity_Color

    """
    return OCC.Quantity.Quantity_Color(r, g, b, OCC.Quantity.Quantity_TOC_RGB)


blue = color(0, 0, 1)
white = color(1, 1, 1)
black = color(0, 0, 0)
gray = color(0.5, 0.5, 0.5)

fp_dark_blue = color(34 / 255, 45 / 255, 90 / 255)
fp_intermediate_blue = color(61 / 255, 79 / 255, 153 / 255)
fp_neon_blue = color(0, 184 / 255, 1)
fp_light_orange = color(1, 136 / 255, 164 / 255)
fp_dark_orange = color(204 / 255, 63 / 255, 20 / 255)

# color sequences
prism_1 = color(0, 12 / 255, 243 / 255)
prism_2 = color(243 / 255, 0, 36 / 255)
prism_3 = color(1, 225 / 255, 0)
prism_4 = color(0, 84 / 255, 171 / 255)
prism_5 = color(198 / 255, 0, 171 / 255)
prism_6 = color(1, 158 / 255, 0)
prism_7 = color(0, 219 / 255, 36 / 255)
prism_8 = color(174 / 255, 0, 243 / 255)
prism_color_sequence = [prism_1, prism_2, prism_3, prism_4, prism_5, prism_6, prism_7, prism_8]

spectral_1 = color(123 / 255, 0, 140 / 255)
spectral_2 = color(0, 0, 209 / 255)
spectral_3 = color(0, 158 / 255, 207 / 255)
spectral_4 = color(0, 157 / 255, 29 / 255)
spectral_5 = color(0, 228 / 255, 0)
spectral_6 = color(224 / 255, 243 / 255, 0)
spectral_7 = color(1, 117 / 255, 0)
spectral_8 = color(208 / 255, 0, 0)
spectral_color_sequence = [spectral_1, spectral_2, spectral_3, spectral_4, spectral_5, spectral_6, spectral_7,
                           spectral_8]

gray_1 = color(0, 0, 0)
gray_2 = color(0.5, 0.5, 0.5)
gray_3 = color(1, 1, 1)
gray_color_sequence = [gray_1, gray_2, gray_3]

