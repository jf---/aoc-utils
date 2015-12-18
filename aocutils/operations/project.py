#!/usr/bin/python
# coding: utf-8

r"""

Functions
---------
point_on_curve
point_on_plane
edge_onto_plane

"""

import OCC.GeomAPI
import OCC.GeomProjLib
import OCC.ProjLib
import OCC.TopoDS

import aocutils.convert.adapt
import aocutils.brep.edge_make


def point_on_curve(crv, pnt):
    r"""Project a point on a curve

    Parameters
    ----------
    crv
    pnt

    Returns
    -------

    """
    if isinstance(crv, OCC.TopoDS.TopoDS_Shape):
        # get the curve handle...
        crv = aocutils.convert.adapt.edge_to_curve(crv).Curve().Curve()
    else:
        raise NotImplementedError('expected a OCC.TopoDS.TopoDS_Edge...')
    rrr = OCC.GeomAPI.GeomAPI_ProjectPointOnCurve(pnt, crv)
    return rrr.LowerDistanceParameter(), rrr.NearestPoint()


def point_on_plane(plane, point):
    r"""Project a point on a plane

    Parameters
    ----------
    plane : Geom_Plane
    point : OCC.gp.gp_Pnt

    Returns
    -------
    OCC.gp.gp_Pnt

    """
    pl = plane.Pln()
    aa, bb = OCC.ProjLib.projlib_Project(pl, point).Coord()
    point = plane.Value(aa, bb)
    return point


def edge_on_plane(edg, plane):
    r"""Project an edge onto a plane

    Parameters
    ----------
    edg : kbe.edge.Edge ??
    plane : Geom_Plane

    Returns
    -------
    TopoDS_Edge
        TopoDS_Edge projected on the plane

    """
    proj = OCC.GeomProjLib.geomprojlib_ProjectOnPlane(edg.adaptor.Curve().Curve(), plane.GetHandle(),
                                                      plane.Axis().Direction(), 1)
    return aocutils.brep.edge_make.edge(proj)
