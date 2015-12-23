#!/usr/bin/python
# coding: utf-8

r"""fixes module

Summary
-------

Various fixing methods for shapes, faces, tolerance, continuity.
Curve resampling

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
import aocutils.geom.curve

logger = logging.getLogger(__name__)


def fix_shape(shp, tolerance=aocutils.tolerance.OCCUTILS_FIXING_TOLERANCE):
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
    fix.SetFixFreeShellMode(True)  # Returns (modifiable) the mode for applying fixes of ShapeFix_Shell, by default True
    sf = fix.FixShellTool().GetObject()
    sf.SetFixOrientationMode(True)
    fix.LimitTolerance(tolerance)
    fix.Perform()  # Iterates on sub- shape and performs fixes.
    return fix.Shape()


def fix_face(face, tolerance=aocutils.tolerance.OCCUTILS_FIXING_TOLERANCE):
    r"""Fix a face

    This operator allows to perform various fixes on face and its wires: fixes provided by ShapeFix_Wire,
    fixing orientation of wires, addition of natural bounds, fixing of missing seam edge,
    and detection and removal of null-area wires.

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

    # Performs all the fixes, depending on modes Function Status returns the status of last call to Perform()
    # ShapeExtend_OK : face was OK, nothing done
    # ShapeExtend_DONE1: some wires are fixed
    # ShapeExtend_DONE2: orientation of wires fixed
    # ShapeExtend_DONE3: missing seam added
    # ShapeExtend_DONE4: small area wire removed
    # ShapeExtend_DONE5: natural bounds added
    # ShapeExtend_FAIL1: some fails during fixing wires
    # ShapeExtend_FAIL2: cannot fix orientation of wires
    # ShapeExtend_FAIL3: cannot add missing seam
    # ShapeExtend_FAIL4: cannot remove small area wire.
    fix.Perform()
    return fix.Face()  # assumes no FixMissingSeam involved


def fix_tolerance(shape, tolerance=aocutils.tolerance.OCCUTILS_DEFAULT_TOLERANCE):
    r"""Sets (enforces) tolerances in a shape to the given value.

    Modifies tolerances of sub-shapes (vertices, edges, faces)

    Parameters
    ----------
    shape : OCC.TopoDS.TopoDS_Shape
    tolerance : float

    """
    # void 	SetTolerance (const TopoDS_Shape &shape, const Standard_Real preci,
    #                     const TopAbs_ShapeEnum styp=TopAbs_SHAPE) const
    OCC.ShapeFix.ShapeFix_ShapeTolerance().SetTolerance(shape, tolerance)


def fix_continuity(edge, continuity=1):
    r"""Fix the continuity of an edge

    Parameters
    ----------
    edge : OCC.TopoDS.TopoDS_Edge
    continuity : int

    Returns
    -------
    OCC.TopoDS.TopoDS_Shape
        The upgrade resulting shape

    """
    # ShapeUpgrade_ShapeDivideContinuity : API Tool for converting shapes with C0 geometry into C1 ones
    shape_upgrade = OCC.ShapeUpgrade.ShapeUpgrade_ShapeDivideContinuity(edge)
    shape_upgrade.SetBoundaryCriterion(eval('OCC.GeomAbs.GeomAbs_C' + str(continuity)))
    shape_upgrade.Perform()
    return shape_upgrade.Result()


def resample_curve_with_uniform_deflection(curve, deflection=0.5, degree_min=3, degree_max=8,
                                           continuity=OCC.GeomAbs.GeomAbs_C2,
                                           tolerance=aocutils.tolerance.OCCUTILS_DEFAULT_TOLERANCE):
    r"""Fits a bspline through the samples on curve

    Parameters
    ----------
    curve : OCC.TopoDS.TopoDS_Wire, OCC.TopoDS.TopoDS_Edge, curve
    deflection : float
    degree_min : int
    degree_max : int
    continuity : OCC.GeomAbs.GeomAbs_C*
    tolerance : float

    Returns
    -------
    OCC.Geom.Geom_Curve
        The resampled curve

    """
    # crv = aocutils.convert.adapt.to_adaptor_3d(curve)
    crv = aocutils.geom.curve.Curve(curve).to_adaptor_3d()
    defl = OCC.GCPnts.GCPnts_UniformDeflection(crv, deflection)
    with aocutils.common.AssertIsDone(defl, 'failed to compute UniformDeflection'):
        logger.info('Number of points : %i' % defl.NbPoints())
    sampled_pnts = [defl.Value(i) for i in range(1, defl.NbPoints())]
    resampled_curve = OCC.GeomAPI.GeomAPI_PointsToBSpline(
        aocutils.collections.point_list_to_tcolgp_array1_of_pnt(sampled_pnts), degree_min, degree_max, continuity,
        tolerance)
    return resampled_curve.Curve().GetObject()
