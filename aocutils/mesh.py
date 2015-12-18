#!/usr/bin/python
# coding: utf-8

r"""mesh.py

Summary
-------
Mashing logic for shapes, based on shape dimensions
"""

import OCC.BRepMesh

import aocutils.analyze.bounds


def mesh(shape, factor=4000.):
    r"""Mesh a shape

    Parameters
    ----------
    shape : OCC.TopoDS.TopoDS_Shape
    factor : float

    """
    bb = aocutils.analyze.bounds.BoundingBox(shape)
    OCC.BRepMesh.BRepMesh_IncrementalMesh(shape, bb.max_dimension / factor)
    # return shape
