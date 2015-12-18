#!/usr/bin/python
# coding: utf-8

r"""
"""

import logging

import OCC.Geom
import OCC.GeomAdaptor
import OCC.Approx
import OCC.BRepAdaptor
import OCC.GeomAbs
import OCC.GeomConvert

import aocutils.common
import aocutils.tolerance
import aocutils.brep.edge_make
import aocutils.exceptions

logger = logging.getLogger(__name__)


class Curve(object):
    r"""
    _curve is a OCC.Geom.Geom_Curve (or subclass)
    """
    def __init__(self, curve):
        if not issubclass(curve.__class__, OCC.Geom.Geom_Curve):
            msg = 'Curve.__init__() needs a Geom_Curve or a subclass, got a %s' % curve.__class__
            logger.critical(msg)
            raise aocutils.exceptions.WrongTopologicalType(msg)
        self._curve = curve

    @classmethod
    def from_handle(cls, handle):
        obj = cls()
        obj._curve = handle.GetObject()
        return obj

    @property
    def handle(self):
        r"""

        Returns
        -------
        Handle< Geom_Curve >

        """
        return self._curve.GetHandle()

    def to_edge(self):
        return aocutils.brep.edge_make.edge(self.handle)

    def to_bspline(self, tolerance=aocutils.tolerance.OCCUTILS_DEFAULT_TOLERANCE, continuity=OCC.GeomAbs.GeomAbs_C1,
                   sections=300, degree=12):
        r"""Convert a curve to a bspline

        Parameters
        ----------
        tolerance : float
        continuity : OCC.GeomAbs.GeomAbs_C*, optional
            (the default is OCC.GeomAbs.GeomAbs_C1)
        sections : int
        degree : int

        Returns
        -------
        Handle< Geom_BSplineCurve >

        """
        approx_curve = OCC.GeomConvert.GeomConvert_ApproxCurve(self.handle, tolerance, continuity, sections, degree)
        with aocutils.common.AssertIsDone(approx_curve, 'could not compute bspline from curve'):
            return approx_curve.Curve()

    def to_adaptor_3d(self):
        r"""Abstract curve like geom_type into an adaptor3d

        Parameters
        ----------
        curve

        Returns
        -------

        """
        return OCC.GeomAdaptor.GeomAdaptor_Curve(self._curve.GetHandle())
