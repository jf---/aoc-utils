#!/usr/bin/python
# coding: utf-8

r"""operations/pipe.py
"""

import OCC.BRepOffsetAPI

import aocutils.common


def pipe(spine, profile):
    r"""Make a pipe

    Parameters
    ----------
    spine : OCC.TopoDS.TopoDS_Wire
    profile : OCC.TopoDS.TopoDS_Wire

    Returns
    -------
    OCC.TopoDS.TopoDS_Shape

    """
    a_pipe = OCC.BRepOffsetAPI.BRepOffsetAPI_MakePipe(spine, profile)
    with aocutils.common.AssertIsDone(a_pipe, 'failed building pipe'):
        a_pipe.Build()
        return a_pipe.Shape()
