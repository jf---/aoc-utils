#!/usr/bin/env python
# coding: utf-8

r"""examples/occutils_surfaces"""

import itertools

import OCC.Display.SimpleGui
import OCC.gp

import aocutils.common
import aocutils.operations.interpolate
import aocutils.brep.face_make
import aocutils.brep.edge_make
import aocutils.brep.vertex_make
import aocutils.brep.wire_make

display, start_display, add_menu, add_function_to_menu = OCC.Display.SimpleGui.init_display("wx")


def n_sided_patch():
    r"""N sided patch"""

    # left
    pts1 = (OCC.gp.gp_Pnt(0, 0, 0.0),
            OCC.gp.gp_Pnt(0, 1, 0.3),
            OCC.gp.gp_Pnt(0, 2, -0.3),
            OCC.gp.gp_Pnt(0, 3, 0.15),
            OCC.gp.gp_Pnt(0, 4, 0),
            )
    # front
    pts2 = (OCC.gp.gp_Pnt(0, 0, 0.0),
            OCC.gp.gp_Pnt(1, 0, -0.3),
            OCC.gp.gp_Pnt(2, 0, 0.15),
            OCC.gp.gp_Pnt(3, 0, 0),
            OCC.gp.gp_Pnt(4, 0, 0),
            )
    # back
    pts3 = (OCC.gp.gp_Pnt(0, 4, 0),
            OCC.gp.gp_Pnt(1, 4, 0.3),
            OCC.gp.gp_Pnt(2, 4, -0.15),
            OCC.gp.gp_Pnt(3, 4, 0),
            OCC.gp.gp_Pnt(4, 4, 1),
            )
    # right
    pts4 = (OCC.gp.gp_Pnt(4, 0, 0),
            OCC.gp.gp_Pnt(4, 1, 0),
            OCC.gp.gp_Pnt(4, 2, 0.3),
            OCC.gp.gp_Pnt(4, 3, -0.15),
            OCC.gp.gp_Pnt(4, 4, 1),
            )

    spl1 = aocutils.operations.interpolate.points_to_bspline(pts1)  # spl1 is a OCC.Geom.Handle_Geom_BSplineCurve
    spl2 = aocutils.operations.interpolate.points_to_bspline(pts2)
    spl3 = aocutils.operations.interpolate.points_to_bspline(pts3)
    spl4 = aocutils.operations.interpolate.points_to_bspline(pts4)

    # list of OCC.TopoDS.TopoDS_Edge
    edges = list(map(aocutils.brep.edge_make.edge, [spl1, spl2, spl3, spl4]))

    # list of OCC.TopoDS.TopoDS_Vertex
    verts = list(map(aocutils.brep.vertex_make.vertex, itertools.chain(pts1, pts2, pts3, pts4)))

    f1 = aocutils.brep.face_make.n_sided(edges, [])  # OCC.TopoDS.TopoDS_Face

    display.DisplayShape(edges)
    display.DisplayShape(verts)
    display.DisplayShape(f1, update=True)

if __name__ == '__main__':
    n_sided_patch()
    start_display()
