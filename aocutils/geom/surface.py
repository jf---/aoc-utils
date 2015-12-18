#!/usr/bin/python
# coding: utf-8

r"""geometry/surface.py
"""

import logging

import OCC.GeomFill

logger = logging.getLogger(__name__)


class Surface(object):
    r"""
    """
    def __init__(self, surface):
        self._surface = surface

    @classmethod
    def from_handle(cls, handle):
        obj = cls()
        obj._surface = handle.GetObject()
        return obj

    @property
    def handle(self):
        r"""

        Returns
        -------
        Handle< Geom_Curve >

        """
        return self._surface.GetHandle()

    @classmethod
    def coons(cls, edges):
        r"""Make coons

        Parameters
        ----------
        edges : list[OCC.TopoDS.TopoDS_Edge]

        Returns
        -------
        Handle< Geom_BSplineSurface >

        """
        if len(edges) == 4:
            spl1, spl2, spl3, spl4 = edges
            srf = OCC.GeomFill.GeomFill_BSplineCurves(spl1, spl2, spl3, spl4, OCC.GeomFill.GeomFill_StretchStyle)
        elif len(edges) == 3:
            spl1, spl2, spl3 = edges
            srf = OCC.GeomFill.GeomFill_BSplineCurves(spl1, spl2, spl3, OCC.GeomFill.GeomFill_StretchStyle)
        elif len(edges) == 2:
            spl1, spl2 = edges
            srf = OCC.GeomFill.GeomFill_BSplineCurves(spl1, spl2, OCC.GeomFill.GeomFill_StretchStyle)
        else:
            msg = 'give 2,3 or 4 curves'
            logger.critical(msg)
            raise ValueError(msg)
        return cls.from_handle(srf.Surface())
