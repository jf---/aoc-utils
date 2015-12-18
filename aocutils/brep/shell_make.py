#!/usr/bin/python
# coding: utf-8

r"""core/shell_make module of occutils
"""

import functools
import logging

# import OCC.BRep
import OCC.BRepBuilderAPI
import OCC.TopoDS
import OCC.ShapeAnalysis

import aocutils.common
import aocutils.topology
import aocutils.brep.base
import aocutils.exceptions

logger = logging.getLogger(__name__)


@functools.wraps(OCC.BRepBuilderAPI.BRepBuilderAPI_MakeShell)
def shell(*args):
    r"""Make a OCC.TopoDS.TopoDS_Shell

    Parameters
    ----------
    args

    Returns
    -------
    OCC.TopoDS.TopoDS_Shell

    Notes
    -----
    BRepBuilderAPI_MakeShell (const Handle< Geom_Surface > &S, const Standard_Boolean Segment=Standard_False)
    BRepBuilderAPI_MakeShell (const Handle< Geom_Surface > &S, const Standard_Real UMin, const Standard_Real UMax,
                              const Standard_Real VMin, const Standard_Real VMax,
                              const Standard_Boolean Segment=Standard_False)

    """
    a_shell = OCC.BRepBuilderAPI.BRepBuilderAPI_MakeShell(*args)
    with aocutils.common.AssertIsDone(a_shell, 'failed to produce shell'):
        result = a_shell.Shell()
        a_shell.Delete()
        return aocutils.topology.shape_to_topology(result)


def shell_from_faces(list_of_faces):
    r"""

    Parameters
    ----------
    list_of_faces : list[OCC.TopoDS.TopoDS_Face]
                 or list[OCC.TopoDS.TopoDS_Shape] where the shape have a TopAbs_FACE type

    Returns
    -------
    OCC.TopoDS.TopoDS_Shell

    """
    if len(list_of_faces) == 0:
        msg = "Cannot build a shell from 0 face"
        logger.error(msg)
        raise aocutils.exceptions.BRepBuildingException(msg)
    builder = OCC.TopoDS.TopoDS_Builder()
    a_shell = OCC.TopoDS.TopoDS_Shell()
    builder.MakeShell(a_shell)
    for face in list_of_faces:
        builder.Add(a_shell, face)
    return a_shell
