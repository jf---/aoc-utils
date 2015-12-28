#!/usr/bin/python
# coding: utf-8

r"""
"""

import logging
import functools

import OCC.BRepBuilderAPI
import OCC.BRep
import OCC.BRepTopAdaptor
import OCC.BRepFill
import OCC.Geom
import OCC.GeomAbs
import OCC.GeomAPI
import OCC.GeomLib
import OCC.GeomPlate
import OCC.TopAbs
import OCC.TopExp
import OCC.TopoDS
import OCC.GeomLProp
import OCC.BRepTools
import OCC.BRepAdaptor
import OCC.ShapeAnalysis
import OCC.GeomProjLib
import OCC.Adaptor3d
import OCC.gp

import aocutils.brep.base
import aocutils.common
import aocutils.brep.edge
import aocutils.brep.wire_make
import aocutils.topology
import aocutils.exceptions

logger = logging.getLogger(__name__)


@functools.wraps(OCC.BRepBuilderAPI.BRepBuilderAPI_MakeFace)
def face(*args):
    r"""Make a OCC.TopoDS.TopoDS_Face

    Parameters
    ----------
    args

    Returns
    -------
    OCC.TopoDS.TopoDS_Face

    """
    a_face = OCC.BRepBuilderAPI.BRepBuilderAPI_MakeFace(*args)
    with aocutils.common.AssertIsDone(a_face, 'failed to produce face'):
        result = a_face.Face()
        a_face.Delete()
        return result


def from_points(points_list):
    r"""Make a face from n points

    Parameters
    ----------
    points_list : list[OCC.gp.gp_Pnt]
    """
    poly = aocutils.brep.wire_make.closed_polygon(points_list)  # poly is a OCC.TopoDS.TopoDS_Wire
    return face(poly)


def ruled(edge_a, edge_b):
    r"""Make a ruled surface between 2 edges

    Parameters
    ----------
    edge_a : OCC.TopoDS.TopoDS_Edge
    edge_b : OCC.TopoDS.TopoDS_Edge

    Returns
    -------
    OCC.TopoDS.TopoDS_Face

    """
    return OCC.BRepFill.brepfill_Face(edge_a, edge_b)


def plane(center=OCC.gp.gp_Pnt(0, 0, 0), vec_normal=OCC.gp.gp_Vec(0, 0, 1), extent_x_min=-100., extent_x_max=100.,
          extent_y_min=-100., extent_y_max=100., depth=0.):
    r"""Make a plane

    Parameters
    ----------
    center : OCC.gp.gp_Pnt
    vec_normal : OCC.gp.gp_Vec
    extent_x_min : float
    extent_x_max : float
    extent_y_min : float
    extent_y_max : float
    depth : float

    Returns
    -------
    OCC.TopoDS.TopoDS_Face

    """
    if depth != 0:
        # noinspection PyUnresolvedReferences
        center = center.add_vec(OCC.gp.gp_Vec(0, 0, depth))
    # noinspection PyUnresolvedReferences
    pln = OCC.gp.gp_Pln(center, OCC.gp.gp_Dir(vec_normal.X(), vec_normal.Y(), vec_normal.Z()))
    a_face = face(pln, extent_x_min, extent_x_max, extent_y_min, extent_y_max)
    return a_face


def n_sided(edges, points, continuity=OCC.GeomAbs.GeomAbs_C0):
    r"""Builds an n-sided patch, respecting the constraints defined by *edges* and *points*

    A simplified call to the BRepFill_Filling class

    It is simplified in the sense that to all constraining edges and points the same level of *continuity*
    will be applied

    Parameters
    ----------
    edges
        the constraining edges
    points
        the constraining points
    continuity : GeomAbs_0, 1, 2
                 GeomAbs_C0 : the surface has to pass by 3D representation of the edge
                 GeomAbs_G1 : the surface has to pass by 3D representation of the edge and to respect tangency with
                 the given face
                 GeomAbs_G2 : the surface has to pass by 3D representation of the edge and to respect tangency and
                 curvature with the given face.

    Returns
    -------
    OCC.TopoDS.TopoDS_Face

    Notes
    -----
    It is not required to set constraining points. Just leave the tuple or list empty

    """
    an_n_sided = OCC.BRepFill.BRepFill_Filling()
    for edg in edges:
        an_n_sided.Add(edg, continuity)
    for pt in points:
        an_n_sided.Add(pt)
    an_n_sided.Build()
    return an_n_sided.Face()


def constrained_surface_from_edges(edges):
    r"""

    DOESNT RESPECT BOUNDARIES

    Parameters
    ----------
    edges : list[OCC.TopoDS.TopoDS_Edge]

    Returns
    -------
    OCC.TopoDS.TopoDS_Face

    """
    bp_srf = OCC.GeomPlate.GeomPlate_BuildPlateSurface(3, 15, 2)
    for edg in edges:
        c = OCC.BRepAdaptor.BRepAdaptor_HCurve()
        c.ChangeCurve().Initialize(edg)
        constraint = OCC.BRepFill.BRepFill_CurveConstraint(c.GetHandle(), 0)
        bp_srf.Add(constraint.GetHandle())
    bp_srf.Perform()
    max_seg, max_deg, crit_order = 9, 8, 0
    tol = 1e-4
    srf = bp_srf.Surface()
    plate = OCC.GeomPlate.GeomPlate_MakeApprox(srf, tol, max_seg, max_deg, tol, crit_order)
    u_min, u_max, v_min, v_max = srf.GetObject().Bounds()
    return face(plate.Surface(), u_min, u_max, v_min, v_max)


def add_wire_to_face(a_face, wire, reverse=False):
    r"""Apply a wire to a a_face
    use reverse to set the orientation of the wire to opposite

    Parameters
    ----------
    a_face
    wire : OCC.TopoDS.TopoDS_Wire
    reverse : bool

    Returns
    -------
    OCC.TopoDS.TopoDS_Face

    """
    a_face = OCC.BRepBuilderAPI.BRepBuilderAPI_MakeFace(a_face)
    if reverse:
        wire.Reverse()
    a_face.Add(wire)
    result = a_face.Face()
    a_face.Delete()
    return result


def from_plane(_geom_plane, lower_limit=-1000, upper_limit=1000):
    r"""Face from a plane

    Parameters
    ----------
    _geom_plane
    lower_limit
    upper_limit

    Returns
    -------
    OCC.TopoDS.TopoDS_Face

    """
    _trim_plane = face(OCC.Geom.Geom_RectangularTrimmedSurface(_geom_plane.GetHandle(), lower_limit, upper_limit,
                                                               lower_limit, upper_limit).GetHandle())
    return _trim_plane
