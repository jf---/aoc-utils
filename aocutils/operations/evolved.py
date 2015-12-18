#!/usr/bin/python
# coding: utf-8

r"""operations/evolved.py"""

import OCC.BRepOffsetAPI

import aocutils.common


def evolved(spine, profile):
    r"""Make an evolved shape

    Parameters
    ----------
    spine : OCC.TopoDS.TopoDS_Wire
    profile : OCC.TopoDS.TopoDS_Wire

    Returns
    -------
    BRepFill_Evolved

    """
    evol = OCC.BRepOffsetAPI.BRepOffsetAPI_MakeEvolved(spine, profile)
    with aocutils.common.AssertIsDone(evol, 'failed building evolved'):
        evol.Build()
        return evol.Evolved()
