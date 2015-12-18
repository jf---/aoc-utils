#!/usr/bin/python
# coding: utf-8

r"""display/color.py
"""

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
