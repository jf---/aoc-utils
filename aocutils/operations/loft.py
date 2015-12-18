#!/usr/bin/python
# coding: utf-8

r"""operations/loft.py
"""

import logging

import OCC.BRepOffsetAPI
import OCC.GeomAbs
import OCC.TopoDS

import aocutils.common
import aocutils.topology
import aocutils.tolerance

logger = logging.getLogger(__name__)


def loft(elements, ruled=False, tolerance=aocutils.tolerance.OCCUTILS_DEFAULT_TOLERANCE,
         continuity=OCC.GeomAbs.GeomAbs_C2, check_compatibility=True):
    r"""Loft

    Parameters
    ----------
    elements
    ruled : bool
    tolerance : float
    continuity : OCC.GeomAbs.GeomAbs_C*, optional
        (the default is OCC.GeomAbs.GeomAbs_C2)
    check_compatibility : bool

    Returns
    -------
    OCC.TopoDS.TopoDS_*

    """
    sections = OCC.BRepOffsetAPI.BRepOffsetAPI_ThruSections(False, ruled, tolerance)
    for i in elements:
        if isinstance(i, OCC.TopoDS.TopoDS_Wire):
            sections.AddWire(i)
        elif isinstance(i, OCC.TopoDS.TopoDS_Vertex):
            sections.AddVertex(i)
        else:
            msg = "elements is a list of OCC.TopoDS.TopoDS_Wire or OCC.TopoDS.TopoDS_Vertex, found a %s " % i.__class__
            logger.error(msg)
            raise TypeError(msg)

    sections.CheckCompatibility(check_compatibility)
    sections.SetContinuity(continuity)
    sections.Build()
    with aocutils.common.AssertIsDone(sections, 'failed lofting'):
        # te = occutils.topology.shape_to_topology()
        return aocutils.topology.shape_to_topology(sections.Shape())
