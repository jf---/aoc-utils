#!/usr/bin/python
# coding: utf-8

r"""operations/extrude.py
"""

import OCC.BRepPrimAPI

import aocutils.common


def extrude(profile, vec):
    r"""Makes a finite prism

    Parameters
    ----------
    profile : OCC.TopoDS.TopoDS_Wire
    vec : OCC.gp.gp_Vec

    Returns
    -------
    OCC.TopoDS.TopoDS_Shape

    """
    pri = OCC.BRepPrimAPI.BRepPrimAPI_MakePrism(profile, vec, True)
    with aocutils.common.AssertIsDone(pri, 'failed building prism'):
        pri.Build()
        return pri.Shape()
