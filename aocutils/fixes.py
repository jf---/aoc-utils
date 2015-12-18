#!/usr/bin/python
# coding: utf-8

r"""

Functions
---------
fix_shape
fix_face
fix_tolerance
fix_continuity
resample_curve_with_uniform_deflection

"""

import logging

import OCC.GCPnts
import OCC.GeomAbs
import OCC.GeomAPI
import OCC.ShapeFix
import OCC.ShapeUpgrade

import aocutils.tolerance
import aocutils.common
import aocutils.collections

logger = logging.getLogger(__name__)


def fix_shape(shp, tolerance=1e-3):
    r"""Fix a shape

    Parameters
    ----------
    shp : OCC.TopoDS.TopoDS_Shape
    tolerance : float

    Returns
    -------
    OCC.TopoDS.TopoDS_Shape

    """
    fix = OCC.ShapeFix.ShapeFix_Shape(shp)
    fix.SetFixFreeShellMode(True)
    sf = fix.FixShellTool().GetObject()
    sf.SetFixOrientationMode(True)
    fix.LimitTolerance(tolerance)
    fix.Perform()
    return fix.Shape()


def fix_face(face, tolerance=1e-3):
    r"""Fix a face

    Parameters
    ----------
    face : ShapeFix_Face
    tolerance : float

    Returns
    -------
    OCC.TopoDS.TopoDS_Face

    """
    fix = OCC.ShapeFix.ShapeFix_Face(face)
    fix.SetMaxTolerance(tolerance)
    fix.Perform()
    return fix.Face()


def fix_tolerance(shape, tolerance=aocutils.tolerance.OCCUTILS_DEFAULT_TOLERANCE):
    r"""Sets (enforces) tolerances in a shape to the given value

    Parameters
    ----------
    shape
    tolerance : float

    """
    OCC.ShapeFix.ShapeFix_ShapeTolerance().SetTolerance(shape, tolerance)


def fix_continuity(edge, continuity=1):
    r"""Fix the continuity of an edge

    Parameters
    ----------
    edge : OCC.TopoDS.topoDS_Edge
    continuity : int

    Returns
    -------
    str
        The upgrade result

    """
    # ShapeUpgrade_ShapeDivideContinuity : API Tool for converting shapes with C0 geometry into C1 ones
    shape_upgrade = OCC.ShapeUpgrade.ShapeUpgrade_ShapeDivideContinuity(edge)
    shape_upgrade.SetBoundaryCriterion(eval('GeomAbs_C' + str(continuity)))
    shape_upgrade.Perform()
    te = str(shape_upgrade.Result())
    return te


def resample_curve_with_uniform_deflection(curve, deflection=0.5, degree_min=3, degree_max=8,
                                           continuity=OCC.GeomAbs.GeomAbs_C2,
                                           tolerance=aocutils.tolerance.OCCUTILS_DEFAULT_TOLERANCE):
    r"""Fits a bspline through the samples on curve

    Parameters
    ----------
    curve : OCC.TopoDS.TopoDS_Wire, OCC.TopoDS.TopoDS_Edge, curve
    deflection
    degree_min
    degree_max
    continuity
    tolerance

    Returns
    -------

    """
    crv = aocutils.convert.adapt.to_adaptor_3d(curve)
    defl = OCC.GCPnts.GCPnts_UniformDeflection(crv, deflection)
    with aocutils.common.AssertIsDone(defl, 'failed to compute UniformDeflection'):
        logger.info('Number of points : %i' % defl.NbPoints())
    sampled_pnts = [defl.Value(i) for i in range(1, defl.NbPoints())]
    resampled_curve = OCC.GeomAPI.GeomAPI_PointsToBSpline(
        aocutils.collections.point_list_to_tcolgp_array1_of_pnt(sampled_pnts), degree_min, degree_max,
        continuity, tolerance)
    return resampled_curve.Curve().GetObject()
