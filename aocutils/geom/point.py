#!/usr/bin/python
# coding: utf-8

r"""geom/point.py
"""

import logging

import operator

import OCC.gp

import aocutils.geom._three_d
import aocutils.tolerance
import aocutils.exceptions

logger = logging.getLogger(__name__)


class Point(aocutils.geom._three_d.ThreeD):
    r"""3D point

    Can be constructed from 3 parameters or from a tuple of length 3

    Examples
    --------
    >>> p = Point.from_xyz(1, 2, 3)
    >>> p.x
    1
    >>> p = Point.from_xyz(x=1, y=2, z=3)
    >>> p.y
    2
    """

    @classmethod
    def from_gp_pnt(cls, gp_pnt):
        obj = cls()
        obj._x = gp_pnt.X()
        obj._y = gp_pnt.Y()
        obj._z = gp_pnt.Z()
        return obj

    @property
    def gp_pnt(self):
        return OCC.gp.gp_Pnt(self.X(), self.Y(), self.Z())

    def translate(self, vector):
        r"""Translate a point with a vector

        Parameters
        ----------
        vector : OCC.gp.gp_Vec or Vector

        Returns
        -------
        OCC.gp.gp_Pnt

        """
        return Point.from_xyz(self.X() + vector.X(), self.Y() + vector.Y(), self.Z() + vector.Z())

    @staticmethod
    def midpoint(pnt_a, pnt_b):
        r"""Computes the point that lies in the middle between pntA and pntB

        Parameters
        ----------
        pnt_a : OCC.gp.gp_Pnt or Point
        pnt_b : OCC.gp.gp_Pnt or Point

        Returns
        -------
        Point

        """
        return Point.from_xyz((pnt_a.X() + pnt_b.X()) / 2., (pnt_a.Y() + pnt_b.Y()) / 2, (pnt_a.Z() + pnt_b.Z()) / 2)

    def middle(self, other):
        r"""Middle of self and other

        Parameters
        ----------
        other : Point
        """
        return Point.from_xyz((self.X() + other.X()) / 2., (self.Y() + other.Y()) / 2., (self.Z() + other.Z()) / 2.)

    def __eq__(self, other):
        r"""Is pnt equal to other?

        Parameters
        ----------
        other : OCC.gp.gp_Pnt or Point

        Returns
        -------
        bool

        """
        if isinstance(other, Point):
            return self.gp_pnt.IsEqual(other.gp_pnt, aocutils.tolerance.OCCUTILS_DEFAULT_TOLERANCE)
        elif isinstance(other, OCC.gp.gp_Pnt):
            return self.gp_pnt.IsEqual(other, aocutils.tolerance.OCCUTILS_DEFAULT_TOLERANCE)
        else:
            msg = "Incompatible point geom_type for comparison"
            logger.critical(msg)
            raise TypeError(msg)
