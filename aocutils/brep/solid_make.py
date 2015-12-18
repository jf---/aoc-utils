#!/usr/bin/python
# coding: utf-8

r"""core/solid.py
"""

import functools

import OCC.BRepBuilderAPI
import OCC.BRepOffsetAPI
import OCC.TopoDS

import aocutils.common
import aocutils.brep.wire_make
import aocutils.brep.edge_make
import aocutils.brep.face_make
import aocutils.operations.transform
import aocutils.operations.sew
# import occutils.convert.gp

# occutils.convert.gp.add_gp_conversions()


@functools.wraps(OCC.BRepBuilderAPI.BRepBuilderAPI_MakeSolid)
def solid(*args):
    r"""Make a OCC.TopoDS.TopoDS_Solid

    Parameters
    ----------
    args

    Returns
    -------
    OCC.TopoDS.TopoDS_Solid

    Notes
    -----
    BRepBuilderAPI_MakeSolid ()
    BRepBuilderAPI_MakeSolid (const TopoDS_CompSolid &S)
    BRepBuilderAPI_MakeSolid (const TopoDS_Shell &S)
    BRepBuilderAPI_MakeSolid (const TopoDS_Shell &S1, const TopoDS_Shell &S2)
    BRepBuilderAPI_MakeSolid (const TopoDS_Shell &S1, const TopoDS_Shell &S2, const TopoDS_Shell &S3)
    BRepBuilderAPI_MakeSolid (const TopoDS_Solid &So)
    BRepBuilderAPI_MakeSolid (const TopoDS_Solid &So, const TopoDS_Shell &S)

    """
    sld = OCC.BRepBuilderAPI.BRepBuilderAPI_MakeSolid(*args)
    with aocutils.common.AssertIsDone(sld, 'failed to produce solid'):
        result = sld.Solid()
        sld.Delete()
        return result


def oriented_box(v_corner, v_x, v_y, v_z):
    r"""Produces an oriented box
    oriented meaning here that the x,y,z axis do not have to be cartesian aligned

    Parameters
    ----------
    v_corner
        the lower corner
    v_x : OCC.gp.gp_Vec
        gp_Vec that describes the X-axis
    v_y : OCC.gp.gp_Vec
        gp_Vec that describes the Y-axis
    v_z : OCC.gp.gp_Vec
        gp_Vec that describes the Z-axis

    Returns
    -------
    OCC.TopoDS.TopoDS_Solid

    """
    verts = map(lambda x: x.as_pnt(), [v_corner, v_corner + v_x, v_corner+v_x+v_y, v_corner+v_y])
    p = aocutils.brep.wire_make.polygon(verts, closed=True)
    li = aocutils.brep.edge_make.line(v_corner.as_pnt(), (v_corner + v_z).as_pnt())
    bmp = OCC.BRepOffsetAPI.BRepOffsetAPI_MakePipe(p, li)
    bmp.Build()
    shp = bmp.Shape()

    bottom = aocutils.brep.face_make.face(p)
    top = aocutils.operations.transform.translate(bottom, v_z, True)
    oriented_bbox = solid(aocutils.operations.sew.sew_shapes([bottom, shp, top]))
    return oriented_bbox
