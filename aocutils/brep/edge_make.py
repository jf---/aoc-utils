#!/usr/bin/python
# coding: utf-8

r"""core/edge_make.py
"""

from __future__ import print_function

import logging
import functools

import OCC.BRepAdaptor
import OCC.BRepBuilderAPI
import OCC.GCPnts
import OCC.Geom
import OCC.TopExp
import OCC.TopoDS
import OCC.gp
import OCC.GeomLProp
import OCC.BRepLProp
import OCC.GeomLib
import OCC.GCPnts
import OCC.GeomAPI
import OCC.ShapeAnalysis
import OCC.BRep
import OCC.BRepIntCurveSurface

import aocutils.common
import aocutils.types
import aocutils.exceptions
import aocutils.math_
import aocutils.operations.interpolate

logger = logging.getLogger(__name__)


@functools.wraps(OCC.BRepBuilderAPI.BRepBuilderAPI_MakeEdge2d)
def edge2d(*args):
    r"""Build an edge

    Parameters
    ----------
    args

    Returns
    -------
    OCC.TopoDS.TopoDS_Edge

    """
    edge = OCC.BRepBuilderAPI.BRepBuilderAPI_MakeEdge2d(*args)
    with aocutils.common.AssertIsDone(edge, 'failed to produce edge'):
        result = edge.Edge()
        edge.Delete()
    return result


@functools.wraps(OCC.BRepBuilderAPI.BRepBuilderAPI_MakeEdge)
def edge(*args):
    r"""Make a OCC.TopoDS.TopoDS_Edge

    Parameters
    ----------
    args

    Returns
    -------
    OCC.TopoDS.TopoDS_Edge

    """
    an_edge = OCC.BRepBuilderAPI.BRepBuilderAPI_MakeEdge(*args)
    with aocutils.common.AssertIsDone(an_edge, 'failed to produce edge'):
        result = an_edge.Edge()
        an_edge.Delete()
        return result


def circle(pnt, radius):
    r"""Make a circle

    Parameters
    ----------
    pnt : OCC.gp.gp_Pnt
        Circle centre
    radius : float

    Returns
    -------
    OCC.TopoDS.TopoDS_Edge

    """
    circ = OCC.gp.gp_Circ()
    circ.SetLocation(pnt)
    circ.SetRadius(radius)
    return edge(circ)


def line(pnt1, pnt2):
    r"""Make a line

    Parameters
    ----------
    pnt1 : OCC.gp.gp_Pnt
    pnt2 : OCC.gp.gp_Pnt

    Returns
    -------
    OCC.TopoDS.TopoDS_Edge

    """
    return edge(pnt1, pnt2)


def geodesic_path(pnt_a, pnt_b, kbe_face, n_segments=20, _tolerance=0.1, n_iter=20):
    r"""

    Parameters
    ----------
    pnt_a
        point to start from
    pnt_b
        point to move towards
    kbe_face
        kbe.face.Face on which `edgA` and `edgB` lie
    n_segments : int
        the number of segments the geodesic is built from
    _tolerance : float
        tolerance when the geodesic is converged
    n_iter : int
        maximum number of iterations

    Returns
    -------
    TopoDS_Edge

    """
    uv_a, srf_pnt_a = kbe_face.project_vertex(pnt_a)
    uv_b, srf_pnt_b = kbe_face.project_vertex(pnt_b)

    path = []
    for i in range(n_segments):
        t = i / n_segments
        u = uv_a[0] + t*(uv_b[0] - uv_a[0])
        v = uv_a[1] + t*(uv_b[1] - uv_a[1])
        path.append(kbe_face.parameter_to_point(u, v))

    def project_pnts(x):
        r"""Project points

        Parameters
        ----------
        x

        Returns
        -------

        """
        return [kbe_face.project_vertex(j)[1] for j in x]

    def poly_length(x):
        r"""Poly length

        Parameters
        ----------
        x

        Returns
        -------

        """
        return sum([x[j].Distance(x[j + 1]) for j in range(len(x) - 1)]) / len(x)

    length = poly_length(path)

    n = 0
    while True:
        path = aocutils.math_.smooth_pnts(path)
        path = project_pnts(path)
        newlength = poly_length(path)
        if abs(newlength-length) < _tolerance or n == n_iter:
            crv = aocutils.operations.interpolate.points_to_bspline(path)
            return edge(crv)
        n += 1
