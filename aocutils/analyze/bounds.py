#!/usr/bin/python
# coding: utf-8

r"""Bounding box analysis

Classes
-------
BoundingBox

"""

import OCC.Bnd
import OCC.BRepBndLib
import OCC.gp

import aocutils.geom.point
import aocutils.tolerance


class BoundingBox(object):
    r"""Wrapper class for a bounding box"""
    def __init__(self, shape, tol=aocutils.tolerance.OCCUTILS_DEFAULT_TOLERANCE):
        self._shape = shape
        self._tol = tol
        self._bbox = OCC.Bnd.Bnd_Box()
        self._bbox.SetGap(tol)
        OCC.BRepBndLib.brepbndlib_Add(shape, self._bbox)
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
