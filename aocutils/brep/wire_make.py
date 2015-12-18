#!/usr/bin/python
# coding: utf-8

r"""core/wire_make.py
"""

import functools

import OCC.BRepBuilderAPI

import aocutils.common


@functools.wraps(OCC.BRepBuilderAPI.BRepBuilderAPI_MakeWire)
def wire(*args):
    r"""Make a OCC.TopoDS.TopoDS_Wire

    Parameters
    ----------
    args

    Returns
    -------
    OCC.TopoDS.TopoDS_Wire

    """
    # if we get an iterable, than add all edges to wire builder
    if isinstance(args[0], list) or isinstance(args[0], tuple):
        a_wire = OCC.BRepBuilderAPI.BRepBuilderAPI_MakeWire()
        for i in args[0]:
            a_wire.Add(i)
        a_wire.Build()
        return a_wire.Wire()

    a_wire = OCC.BRepBuilderAPI.BRepBuilderAPI_MakeWire(*args)
    a_wire.Build()
    with aocutils.common.AssertIsDone(a_wire, 'failed to produce wire'):
        result = a_wire.Wire()
        return result


@functools.wraps(OCC.BRepBuilderAPI.BRepBuilderAPI_MakePolygon)
def polygon(args, closed=False):
    r"""Make a polygon

    Parameters
    ----------
    args
    closed : bool

    Returns
    -------
    OCC.TopoDS.TopoDS_Wire

    """
    poly = OCC.BRepBuilderAPI.BRepBuilderAPI_MakePolygon()
    for pt in args:
        # support nested lists
        if isinstance(pt, list) or isinstance(pt, tuple):
            for i in pt:
                poly.Add(i)
        else:
            poly.Add(pt)
    if closed:
        poly.Close()
    poly.Build()

    with aocutils.common.AssertIsDone(poly, 'failed to produce wire'):
        result = poly.Wire()
        return result


@functools.wraps(OCC.BRepBuilderAPI.BRepBuilderAPI_MakePolygon)
def closed_polygon(*args):
    r"""Make a closed polygon

    Parameters
    ----------
    args

    Returns
    -------
    OCC.TopoDS.TopoDS_Wire

    """
    poly = OCC.BRepBuilderAPI.BRepBuilderAPI_MakePolygon()
    for pt in args:
        if isinstance(pt, list) or isinstance(pt, tuple):
            for i in pt:
                poly.Add(i)
        else:
            poly.Add(pt)
    poly.Build()
    poly.Close()
    with aocutils.common.AssertIsDone(poly, 'failed to produce wire'):
        result = poly.Wire()
        return result
