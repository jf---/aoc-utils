#!/usr/bin/python
# coding: utf-8

r"""face.py module example use"""

from __future__ import print_function

import OCC.BRepPrimAPI

import aocutils.brep.face


if __name__ == "__main__":
    # BRepPrimAPI_MakeSphere(<params>).Face() in inherited from BRepPrimAPI_MakeOneAxis
    # Face() returns the lateral face of the rotational primitive.
    sphere_face = OCC.BRepPrimAPI.BRepPrimAPI_MakeSphere(1, 1).Face()
    occutils_wrapped_sphere_face = aocutils.brep.face.Face(sphere_face)

    print(occutils_wrapped_sphere_face.topo)
    print(occutils_wrapped_sphere_face.topo_type)
    print(occutils_wrapped_sphere_face.is_trimmed())
    print(occutils_wrapped_sphere_face.is_valid())
    print(occutils_wrapped_sphere_face.is_dirty)
    # print(occutils_wrapped_sphere_face.is_planar())  # Fails -> investigate
