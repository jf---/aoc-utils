#!/usr/bin/python
# coding: utf-8

r"""operations/trim.py
"""

import warnings
import logging

import OCC.Geom

import aocutils.brep.edge_make
import aocutils.brep.wire
import aocutils.operations.project


logger = logging.getLogger(__name__)


def trim_wire(wire, shape_limit_1, shape_limit_2, periodic=False):
    r"""Trim wire

    Parameters
    ----------
    wire : OCC.TopoDS.TopoDS_Wire
    shape_limit_1
    shape_limit_2
    periodic

    Returns
    -------
    TopoDS_Edge
        the trimmed wire that lies between `shapeLimit1` and `shapeLimit2`

    """
    adap = aocutils.brep.wire.Wire(wire).to_adaptor_3d()
    bspl = adap.BSpline()

    if periodic:
        spl = bspl.GetObject()
        if spl.IsClosed():
            spl.SetPeriodic()
        else:
            msg = "the wire to be trimmed is not closed, hence cannot be made periodic"
            logger.warn(msg)
            warnings.warn(msg)

    p1 = aocutils.operations.project.point_on_curve(bspl, shape_limit_1)[0]
    p2 = aocutils.operations.project.point_on_curve(bspl, shape_limit_2)[0]
    a, b = sorted([p1, p2])
    tr = OCC.Geom.Geom_TrimmedCurve(bspl, a, b).GetHandle()
    return aocutils.brep.edge_make.edge(tr)
