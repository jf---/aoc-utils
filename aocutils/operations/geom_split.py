#!/usr/bin/python
# coding: utf-8

r"""
This modules makes the construction of geometry a little easier with the help of the GEOM library.

Functions
---------
splitter

"""

from __future__ import with_statement
from __future__ import print_function

try:
    from OCC.GEOMAlgo import GEOMAlgo_Splitter
except ImportError:
    print("GEOM wrapper is necessary to access advanced constructs.")
    raise


def splitter(shape, profile):
    r"""split a shape using a profile

    Parameters
    ----------
    shape
    profile

    Returns
    -------
    the splitted shape

    """
    split = GEOMAlgo_Splitter()
    split.AddShape(shape)
    split.AddTool(profile)
    split.Perform()
    splitter_shape = split.Shape()
    return splitter_shape
