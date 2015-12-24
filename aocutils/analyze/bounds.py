#!/usr/bin/python
# coding: utf-8

r"""Bounding box analysis

"""

import logging

import OCC.Bnd
import OCC.BRepBndLib
import OCC.gp
import OCC.TopoDS

import aocutils.geom.point
import aocutils.tolerance
import aocutils.exceptions
import aocutils.brep.base
import aocutils.mesh

logger = logging.getLogger(__name__)


class BoundingBox(object):
    r"""Wrapper class for a bounding box

    Notes
    -----
    Mesh the shape before instantiating a BoundingBox if required, infinite recursion would be created by calling
    mesh.py's mesh() method

    """
    def __init__(self, shape, tol=aocutils.tolerance.OCCUTILS_DEFAULT_TOLERANCE):
        if isinstance(shape, OCC.TopoDS.TopoDS_Shape) or issubclass(shape.__class__, OCC.TopoDS.TopoDS_Shape):
            self._shape = shape
        else:
            msg = "Expecting a TopoDS_Shape (or a subclass), got a %s" % str(shape.__class__)
            logger.error(msg)
            raise aocutils.exceptions.WrongTopologicalType(msg)
        # self._shape = shape
        self._tol = tol
        self._bbox = OCC.Bnd.Bnd_Box()
        self._bbox.SetGap(tol)
        OCC.BRepBndLib.brepbndlib_Add(self._shape, self._bbox)
        self.x_min, self.y_min, self.z_min, self.x_max, self.y_max, self.z_max = self._bbox.Get()

    @property
    def bnd_box(self):
        r"""The OCC bounding box object

        Returns
        -------
        OCC.Bnd.Bnd_Box

        """
        return self._bbox

    @property
    def x_span(self):
        r"""x dimension of bounding box"""
        return self.x_max - self.x_min

    @property
    def y_span(self):
        r"""y dimension of bounding box"""
        return self.y_max - self.y_min

    @property
    def z_span(self):
        r"""z dimension of bounding box"""
        return self.z_max - self.z_min

    @property
    def max_dimension(self):
        r"""Maximum dimension"""
        return max([self.x_span, self.y_span, self.z_span])

    @property
    def min_dimension(self):
        r"""Minimum dimension"""
        return min([self.x_span, self.y_span, self.z_span])

    @property
    def aspect_ration(self):
        r"""Aspect ratio"""
        return self.max_dimension / self.min_dimension

    @property
    def as_tuple(self):
        r"""bounding box as the original tuple"""
        return self.x_min, self.y_min, self.z_min, self.x_max, self.y_max, self.z_max

    @property
    def centre(self):
        r"""

        Returns
        -------
        OCC.gp.gp_Pnt

        """
        return aocutils.geom.point.Point.midpoint(OCC.gp.gp_Pnt(self.x_min, self.y_min, self.z_min),
                                                  OCC.gp.gp_Pnt(self.x_max, self.y_max, self.z_max))
