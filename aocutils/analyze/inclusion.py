#!/usr/bin/python
# coding: utf-8

r"""

Functions
---------
point_in_boundingbox
point_in_solid

"""

import logging

import OCC.BRepClass3d
import OCC.TopAbs

import aocutils.analyze.bounds
import aocutils.types
import aocutils.exceptions
import aocutils.tolerance

logger = logging.getLogger(__name__)


def point_in_boundingbox(shape, pnt, tolerance=aocutils.tolerance.OCCUTILS_DEFAULT_TOLERANCE):
    r"""Is pnt inside the bounding box of solid?

    This is a much speedier test than checking the TopoDS_Solid

    Parameters
    ----------
    shape : TopoDS_Shape
    pnt : OCC.gp.gp_Pnt
    tolerance : float

    Returns
    -------
    bool
        True if pnt lies in boundingbox, False otherwise

    """
    return not aocutils.analyze.bounds.BoundingBox(shape, tolerance).bnd_box.IsOut(pnt)


def point_in_solid(shape, pnt, tolerance=aocutils.tolerance.OCCUTILS_DEFAULT_TOLERANCE):
    r"""Is pnt inside solid?

    Parameters
    ----------
    solid : TopoDS_Solid
    pnt : OCC.gp.gp_Pnt
    tolerance : float

    Returns
    -------
    bool
        True if pnt lies in solid, False otherwise

    """
    if aocutils.types.topo_lut[shape.ShapeType()] not in ["compound", "compsolid", "solid", "shell"]:
        msg = "Cannot evaluate in/out position of a point in a 2D or less shape"
        logger.error(msg)
        raise aocutils.exceptions.WrongTopologicalType(msg)

    _in_solid = OCC.BRepClass3d.BRepClass3d_SolidClassifier(shape, pnt, tolerance)
    logger.info('State : %s' % str(_in_solid.State()))
    if _in_solid.State() == OCC.TopAbs.TopAbs_ON:
        return None
    if _in_solid.State() == OCC.TopAbs.TopAbs_OUT:
        return False
    if _in_solid.State() == OCC.TopAbs.TopAbs_IN:
        return True
