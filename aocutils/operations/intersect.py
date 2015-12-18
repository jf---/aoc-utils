#!/usr/bin/python
# coding: utf-8

r"""

Functions
---------
from_three_planes
shape_by_line

"""

import OCC.IntAna
import OCC.IntCurvesFace

import aocutils.common
import aocutils.tolerance


def from_three_planes(plane_a, plane_b, plane_c):
    r"""Intersection from 3 planes

    Accepts both Geom_Plane and gp_Pln

    Parameters
    ----------
    plane_a
    plane_b
    plane_c

    Returns
    -------
    OCC.gp.gp_Pnt

    """
    plane_a = plane_a if not hasattr(plane_a, 'Pln') else plane_a.Pln()
    plane_b = plane_b if not hasattr(plane_b, 'Pln') else plane_b.Pln()
    plane_c = plane_c if not hasattr(plane_c, 'Pln') else plane_c.Pln()

    intersection_planes = OCC.IntAna.IntAna_Int3Pln(plane_a, plane_b, plane_c)
    pnt = intersection_planes.Value()
    return pnt


def shape_by_line(topods_shape, line, low_parameter=0.0, hi_parameter=float("+inf")):
    r"""Finds the intersection of a shape and a line

    Parameters
    ----------
    topods_shape : any TopoDS_*
    line : gp_Lin
    low_parameter : float, optional
        (the default value is 0.0)
    hi_parameter : float, optional
        (the default value is infinity)

    Returns
    -------
    a list with a number of tuples that corresponds to the number of intersections found
    the tuple contains ( OCC.gp.gp_Pnt, TopoDS_Face, u,v,w ), respectively the intersection point, the intersecting face
    and the u,v,w parameters of the intersection point
    """
    shape_inter = OCC.IntCurvesFace.IntCurvesFace_ShapeIntersector()
    shape_inter.Load(topods_shape, aocutils.tolerance.OCCUTILS_DEFAULT_TOLERANCE)
    shape_inter.PerformNearest(line, low_parameter, hi_parameter)

    with aocutils.common.AssertIsDone(shape_inter, "failed to computer shape / line intersection"):
        return (shape_inter.Pnt(1),
                shape_inter.Face(1),
                shape_inter.UParameter(1),
                shape_inter.VParameter(1),
                shape_inter.WParameter(1))
