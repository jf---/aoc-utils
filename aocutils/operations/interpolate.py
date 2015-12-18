#!/usr/bin/python
# coding: utf-8

r"""Interpolation

Functions
---------
filter_points_by_distance
points_to_bspline
points
points_vectors
points_no_tangency

Notes
-----
OCC.GeomAPI.GeomAPI_PointsToBSpline
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
This class is used to approximate a BsplineCurve passing through an array of points, with a given Continuity. Describes
functions for building a 3D BSpline curve which approximates a set of points.
A PointsToBSpline object provides a framework for:
- defining the data of the BSpline curve to be built,
- implementing the approximation algorithm, and consulting the results.

OCC.GeomAPI.GeomAPI_Interpolate
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
This class is used to interpolate a BsplineCurve passing through an array of points, with a C2 Continuity if tangency
is not requested at the point. If tangency is requested at the point the continuity will be C1.
If Perodicity is requested the curve will be closed and the junction will be the first point given.
The curve will than be only C1 Describes functions for building a constrained 3D BSpline curve.
The curve is defined by a table of points through which it passes, and if required:
- by a parallel table of reals which gives the value of the parameter of each point through which the resulting
  BSpline curve passes, and
- by vectors tangential to these points. An Interpolate object provides a framework for:
- defining the constraints of the BSpline curve,
- implementing the interpolation algorithm, and
- consulting the results.

"""

import logging

import OCC.GeomAPI
import OCC.TColgp
import OCC.TColStd

import aocutils.exceptions
import aocutils.tolerance
import aocutils.collections

logger = logging.getLogger(__name__)


def filter_points_by_distance(list_of_point, distance=0.1):
    r"""Get rid of those point that lie within tolerance of a consecutive series of points

    Parameters
    ----------
    list_of_point : list[OCC.gp.gp_Pnt]
        List of gp_Pnt
    distance : float, optional
        (the default value is 0.1)

    Returns
    -------
    list
        Filtered list of gp_Pnt

    """
    tmp = [list_of_point[0]]
    for a in list_of_point[1:]:
        if any([a.IsEqual(i, distance) for i in tmp]):
            continue
        else:
            tmp.append(a)
    return tmp


def points_to_bspline(pnts):
    r"""Points to bspline

    Parameters
    ----------
    pnts : list[OCC.gp.gp_Pnt]
        List of points to create the bspline

    Returns
    -------
    OCC.Geom.Handle_Geom_BSplineCurve

    """
    pnts = aocutils.collections.point_list_to_tcolgp_array1_of_pnt(pnts)
    crv = OCC.GeomAPI.GeomAPI_PointsToBSpline(pnts)
    return crv.Curve()


# def fix(li, _type):
#     r"""function factory for 1-dimensional TCol* types
#
#     Parameters
#     ----------
#     li
#     _type
#
#     Returns
#     -------
#
#     """
#     pts = _type(1, len(li))
#     for n, i in enumerate(li):
#         pts.SetValue(n+1, i)
#     pts.thisown = False
#     return pts


def points(list_of_points, start_tangent, end_tangent, filter_pts=True,
           tolerance=aocutils.tolerance.OCCUTILS_DEFAULT_TOLERANCE):
    r"""Interpolate points

    Parameters
    ----------
    list_of_points : list[OCC.gp.gp_Pnt]
    start_tangent : OCC.gp.gp_Vec
    end_tangent : OCC.gp.gp_Vec
    filter_pts : bool
    tolerance : float

    Returns
    -------
    OCC.Geom.Handle_Geom_BSplineCurve

    """

    if filter_pts:
        list_of_points = filter_points_by_distance(list_of_points)

    fixed_points = aocutils.convert.collections.tcol_dim_1(list_of_points, OCC.TColgp.TColgp_HArray1OfPnt,
                                                           start_at_one=True)
    try:
        interp = OCC.GeomAPI.GeomAPI_Interpolate(fixed_points.GetHandle(), False, tolerance)
        interp.Load(start_tangent, end_tangent, False)
        interp.Perform()
        if interp.IsDone():
            return interp.Curve()
    except RuntimeError:
        msg = 'Failed to interpolate the shown points'
        logger.error(msg)
        raise aocutils.exceptions.InterpolationException(msg)


def points_vectors(list_of_points, list_of_vectors, vector_mask=None,
                   tolerance=aocutils.tolerance.OCCUTILS_DEFAULT_TOLERANCE):
    r"""Build a curve from a set of points and vectors the vectors describe the tangent vector
    at the corresponding point

    Parameters
    ----------
    list_of_points : list[OCC.gp.gp_Pnt]
    list_of_vectors : list[OCC.gp.gp_Vec]
    vector_mask
    tolerance : float

    Returns
    -------

    """
    # OCC.GeomAPI.GeomAPI_Interpolate is buggy: need to use `fix` in order to get the right points in...
    assert len(list_of_points) == len(list_of_vectors), 'vector and point list not of same length'

    if vector_mask is not None:
        assert len(vector_mask) == len(list_of_points), 'length vector mask is not of length points list nor []'
    else:
        vector_mask = [True for _ in range(len(list_of_points))]

    fixed_mask = aocutils.convert.collections.tcol_dim_1(vector_mask, OCC.TColStd.TColStd_HArray1OfBoolean,
                                                         start_at_one=True)
    fixed_points = aocutils.convert.collections.tcol_dim_1(list_of_points, OCC.TColgp.TColgp_HArray1OfPnt,
                                                           start_at_one=True)
    fixed_vectors = aocutils.convert.collections.tcol_dim_1(list_of_vectors, OCC.TColgp.TColgp_Array1OfVec,
                                                            start_at_one=True)

    try:
        interp = OCC.GeomAPI.GeomAPI_Interpolate(fixed_points.GetHandle(), False, tolerance)
        interp.Load(fixed_vectors, fixed_mask.GetHandle(), False)
        interp.Perform()
        if interp.IsDone():
            return interp.Curve()
    except RuntimeError:
        # the exception was unclear
        msg = 'Failed to interpolate the points'
        logger.error(msg)
        raise aocutils.exceptions.InterpolationException(msg)


def points_no_tangency(list_of_points, filter_pts=True, closed=False,
                       tolerance=aocutils.tolerance.OCCUTILS_DEFAULT_TOLERANCE):
    r"""OCC.GeomAPI.GeomAPI_Interpolate is buggy: need to use `fix` in order to get the right points in...

    Parameters
    ----------
    list_of_points : list[OCC.gp.gp_Pnt]
    filter_pts : bool
    closed : bool
    tolerance : float

    Returns
    -------

    """

    if filter_pts:
        list_of_points = filter_points_by_distance(list_of_points)

    fixed_points = aocutils.convert.collections.tcol_dim_1(list_of_points, OCC.TColgp.TColgp_HArray1OfPnt,
                                                           start_at_one=True)
    try:
        interp = OCC.GeomAPI.GeomAPI_Interpolate(fixed_points.GetHandle(), closed, tolerance)
        interp.Perform()
        if interp.IsDone():
            return interp.Curve()

    except RuntimeError:
        # the exception was unclear
        msg = 'Failed to interpolate the points'
        logger.error(msg)
        raise aocutils.exceptions.InterpolationException(msg)
