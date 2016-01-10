#!/usr/bin/python
# coding: utf-8

r"""primitives.py

Summary
-------

Simple shapes creation: box, sphere etc ....

"""

from __future__ import division

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
    with aocutils.common.AssertIsDone(a_box, 'failed to build a cube...'):
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
    with aocutils.common.AssertIsDone(a_sphere, 'failed to build a sphere...'):
        return a_sphere.Shape()


@functools.wraps(OCC.BRepPrimAPI.BRepPrimAPI_MakeCylinder)
def cylinder(*args):
    r"""Make a cylinder

    Parameters
    ----------
    args

    Returns
    -------
    OCC.TopoDS.TopoDS_Shape

    """
    a_cylinder = OCC.BRepPrimAPI.BRepPrimAPI_MakeCylinder(*args)
    a_cylinder.Build()
    with aocutils.common.AssertIsDone(a_cylinder, 'failed to build a cylinder...'):
        return a_cylinder.Shape()


def tube(outer_diameter, inner_diameter, length):
    r"""Make a tube

    Parameters
    ----------
    outer_diameter
    inner_diameter
    length

    Returns
    -------
    OCC.TopoDS.TopoDS_Shape

    """
    import aocutils.operations.boolean

    out_cylinder = OCC.BRepPrimAPI.BRepPrimAPI_MakeCylinder(outer_diameter / 2., length)
    out_cylinder.Build()
    with aocutils.common.AssertIsDone(out_cylinder, 'failed to build the outer cylinder...'):
        shape_a = out_cylinder.Shape()

    in_cylinder = OCC.BRepPrimAPI.BRepPrimAPI_MakeCylinder(inner_diameter / 2., length)
    in_cylinder.Build()
    with aocutils.common.AssertIsDone(in_cylinder, 'failed to build the inner cylinder...'):
        shape_b = in_cylinder.Shape()

    return aocutils.operations.boolean.cut(shape_a, shape_b)
