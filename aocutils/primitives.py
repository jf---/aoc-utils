#!/usr/bin/python
# coding: utf-8

r"""primitives.py

Summary
-------

Simple shapes creation: box, sphere etc ....

"""

import functools

import OCC.BRepPrimAPI

import aocutils.common


@functools.wraps(OCC.BRepPrimAPI.BRepPrimAPI_MakeBox)
def box(*args):
    r"""Make a box

    Parameters
    ----------
    args

    Returns
    -------
    OCC.TopoDS.TopoDS_Shape

    """
    a_box = OCC.BRepPrimAPI.BRepPrimAPI_MakeBox(*args)
    a_box.Build()
    with aocutils.common.AssertIsDone(a_box, 'failed to built a cube...'):
        return a_box.Shape()


@functools.wraps(OCC.BRepPrimAPI.BRepPrimAPI_MakeSphere)
def sphere(*args):
    r"""Make a sphere

    Parameters
    ----------
    args

    Returns
    -------
    OCC.TopoDS.TopoDS_Shape

    """
    a_sphere = OCC.BRepPrimAPI.BRepPrimAPI_MakeSphere(*args)
    a_sphere.Build()
    with aocutils.common.AssertIsDone(a_sphere, 'failed to built a sphere...'):
        return a_sphere.Shape()
