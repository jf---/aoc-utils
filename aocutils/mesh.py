#!/usr/bin/python
# coding: utf-8

r"""mesh.py

Summary
-------
Meshing logic for shapes, based on shape dimensions

Notes
-----

BRepMesh_IncrementalMesh (const TopoDS_Shape &theShape, const Standard_Real theLinDeflection,
                          const Standard_Boolean isRelative=Standard_False, const Standard_Real theAngDeflection=0.5,
                          const Standard_Boolean isInParallel=Standard_False)
"""

import OCC.BRepMesh

import aocutils.analyze.bounds


def mesh(shape, factor=4000., use_min_dim=False):
    r"""Mesh a shape

    Parameters
    ----------
    shape : OCC.TopoDS.TopoDS_Shape
        Shape to mesh
    factor : float
        The higher, the finer the mesh
    use_min_dim : bool (optional)
        Use minimum bounding box dimension to compute the linear deflection.
        The default is False (i.e. use max dimension)
        This is useful for long and thin objects where using the max dimension would result in a very coarse linear
        deflection in the other directions.

    """
    bb = aocutils.analyze.bounds.BoundingBox(shape)
    if use_min_dim:
        OCC.BRepMesh.BRepMesh_IncrementalMesh(shape, bb.min_dimension / factor)
    else:
        OCC.BRepMesh.BRepMesh_IncrementalMesh(shape, bb.max_dimension / factor)
    # return shape
