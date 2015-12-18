#!/usr/bin/python
# coding: utf-8

r"""core/vertex_make.py
"""

import functools
import logging

import OCC.BRepBuilderAPI
import OCC.gp
import OCC.TopoDS
import OCC.TopExp
import OCC.ShapeBuild

import aocutils.common
import aocutils.exceptions
import aocutils.brep.base

logger = logging.getLogger(__name__)


@functools.wraps(OCC.BRepBuilderAPI.BRepBuilderAPI_MakeVertex)
def vertex(*args):
    r"""Make a OCC.TopoDS.TopoDS_Vertex

    Parameters
    ----------
    args

    Returns
    -------
    OCC.TopoDS.TopoDS_Vertex

    """
    vert = OCC.BRepBuilderAPI.BRepBuilderAPI_MakeVertex(*args)
    with aocutils.common.AssertIsDone(vert, 'failed to produce vertex'):
        result = vert.Vertex()
        vert.Delete()
        return result


def common_vertex(edg1, edg2):
    r"""Common vertex of 2 edges

    Parameters
    ----------
    edg1 : OCC.TopoDS.TopoDS_Edge
    edg2 : OCC.TopoDS.TopoDS_Edge

    Returns
    -------
    OCC.TopoDS.TopoDS_Vertex
        The common vertex of 2 edges

    """
    vert = OCC.TopoDS.TopoDS_Vertex()
    if OCC.TopExp.topexp_CommonVertex(edg1, edg2, vert):
        return vert
    else:
        msg = "No common vertex found"
        logger.error(msg)
        raise aocutils.exceptions.NoCommonVertexException(msg)
