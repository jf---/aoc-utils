#!/usr/bin/python
# coding: utf-8

r"""
"""


class ThreeD(object):
    r"""3 dimensional object with x y z coordinates"""
    @classmethod
    def from_xyz(cls, x, y, z):
        r"""Create from 3 numbers

        Parameters
        ----------
        x : int or float
        y : int or float
        z : int of float

        """
        obj = cls()
        obj._x = x
        obj._y = y
        obj._z = z
        return obj

    @classmethod
    def from_tuple(cls, tpl):
        r"""Create from a tuple of length 3

        Parameters
        ----------
        tpl : tuple[int or float]
            Tuple of length 3
        """
        obj = cls()
        obj._x = tpl[0]
        obj._y = tpl[1]
        obj._z = tpl[2]
        return obj

    # X() Y() and Z() are intentionally not properties to behave as a gp_Pnt
    def X(self):
        r"""x coordinate"""
        return self._x

    def Y(self):
        r"""y coordinate"""
        return self._y

    def Z(self):
        r"""z coordinate"""
        return self._z

    @property
    def x(self):
        r"""x coordinate"""
        return self._x

    @property
    def y(self):
        r"""y coordinate"""
        return self._y

    @property
    def z(self):
        r"""z coordinate"""
        return self._z
