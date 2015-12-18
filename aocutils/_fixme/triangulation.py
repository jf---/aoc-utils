# coding=utf-8

r"""
Triangulation
"""

from __future__ import print_function

import OCC.BRepMesh
import OCC.Bnd
import OCC.BRepBndLib
import OCC.TopTools
# from OCC.TopoDS import *

import aocutils.common
import aocutils.topology


def vertices_faces_from_shape(shape, deflection=0.1):
    r"""Vertices and faces of the mesh that represents the BREP

    Parameters
    ----------
    shape: TopoDS_Shape

    """
    list_of_shape = OCC.TopTools.TopTools_ListOfShape()
    list_of_shape.Append(shape)

    indexed_data_map_of_shape_list_of_shape = OCC.TopTools.TopTools_IndexedDataMapOfShapeListOfShape()
    indexed_data_map_of_shape_list_of_shape.Add(shape, list_of_shape)

    bbox = OCC.Bnd.Bnd_Box()
    bbox.SetGap(1e-6)
    OCC.BRepBndLib.brepbndlib_Add(shape, bbox)

    # These arguments are *SO* random...
    fd = OCC.BRepMesh.BRepMesh_FastDiscret(0.1, 0.1, bbox, False, False, False, False)
    for f in aocutils.topology.Topo(shape).faces():
        fd.Add(f, indexed_data_map_of_shape_list_of_shape)
    n_vert, n_edge, n_face = fd.NbVertices(), fd.NbEdges(), fd.NbTriangles()
    print('number of mesh vertices, edges, triangles representing the BREP:', n_vert, n_edge, n_face)
    tris = [fd.Triangle(i) for i in range(1, fd.NbTriangles())]
    verts = [fd.Vertex(i) for i in range(1, fd.NbVertices())]


if __name__ == '__main__':
    from OCC.BRepPrimAPI import *
    sphere = BRepPrimAPI_MakeSphere(1).Shape()
    vertices_faces_from_shape(sphere)
