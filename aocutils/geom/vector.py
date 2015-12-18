#!/usr/bin/python
# coding: utf-8

r"""geom/vector.py
"""

from __future__ import division

import logging

import OCC.gp

import aocutils.tolerance
import aocutils.exceptions

logger = logging.getLogger(__name__)


class Vector(object):
    def __init__(self, x, y, z):
        self._x = x
        self._y = z
        self._z = z

    @classmethod
    def from_gp_vec(cls, gp_vec):
        obj = cls()
        obj._x = gp_vec.X()
        obj._y = gp_vec.Y()
        obj._z = gp_vec.Z()
        return obj

    @property
    def gp_vec(self):
        return OCC.gp.gp_Vec(self.X(), self.Y(), self.Z())

    def X(self):
        return self._x

    def Y(self):
        return self._y

    def Z(self):
        return self._z

    def norm(self):
        return (self._x**2 + self._y**2 + self.z**2)**.5

    def __add__(self, other):
        r"""Add a vector to self

        Parameters
        ----------
        other : OCC.gp.gp_Vec or Vector

        Returns
        -------
        Vector

        """
        return Vector(self.X() + other.X(), self.Y() + other.Y(), self.Z() + other.Z())

    def __sub__(self, other):
        r"""Substract a vector to self

        Parameters
        ----------
        other : OCC.gp.gp_Vec or Vector

        Returns
        -------
        Vector

        """
        return Vector(self.X() - other.X(), self.Y() - other.Y(), self.Z() - other.Z())

    def __mul__(self, scalar):
        r"""Multiply a vector by a scalar

        Parameters
        ----------
        scalar : float

        Returns
        -------
        Vector

        """
        return Vector(self.X() * scalar, self.Y() * scalar,  self.Z() * scalar)

    def __div__(self, scalar):
        r"""Multiply a vector by a scalar

        Parameters
        ----------
        scalar : float

        Returns
        -------
        Vector

        """
        return Vector(self.X() / scalar, self.Y() / scalar,  self.Z() / scalar)

    def __eq__(self, other):
        r"""Is self equal to other?

        Parameters
        ----------
        other : OCC.gp.gp_Pnt or Point

        Returns
        -------
        bool

        """
        if isinstance(other, Vector):
            return self.gp_vec.IsEqual(other.gp_vec, aocutils.tolerance.OCCUTILS_DEFAULT_TOLERANCE)
        elif isinstance(other, OCC.gp.gp_Pnt):
            return self.gp_vec.IsEqual(other, aocutils.tolerance.OCCUTILS_DEFAULT_TOLERANCE)
        else:
            msg = "Incompatible vector geom_type for comparison"
            logger.critical(msg)
            raise TypeError(msg)

    def to_dir(self):
        r"""Convert a gp_Vec to a gp_Dir

        Returns
        -------
        OCC.gp.gp_Dir

        """
        return OCC.gp.gp_Dir(self.gp_vec)
