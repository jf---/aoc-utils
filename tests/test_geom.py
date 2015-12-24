#!/usr/bin/python
# coding: utf-8

r"""
"""

import sys

import pytest

import OCC.BRepPrimAPI
import OCC.Geom

import aocutils.brep.wire
import aocutils.topology
import aocutils.geom.curve
import aocutils.geom.point
import aocutils.geom.vector

PY3 = not (int(sys.version.split('.')[0]) <= 2)


@pytest.fixture()
def box_shape():
    r"""Box shape for testing"""
    return OCC.BRepPrimAPI.BRepPrimAPI_MakeBox(10, 20, 30).Shape()


def test_curve(box_shape):
    t = aocutils.topology.Topo(box_shape)
    wire = t.wires.__next__() if PY3 else t.wires.next()

    curve = aocutils.brep.wire.Wire(wire).to_curve()
    assert isinstance(curve, OCC.Geom.Geom_BSplineCurve)
    assert issubclass(curve.__class__, OCC.Geom.Geom_Curve)

    bspline = aocutils.geom.curve.Curve(curve).to_bspline()
    assert isinstance(bspline, OCC.Geom.Handle_Geom_BSplineCurve)
    assert isinstance(bspline.GetObject(), OCC.Geom.Geom_BSplineCurve)


def test_point_middle():
    p1 = aocutils.geom.point.Point.from_xyz(0, 0, 0)
    p2 = aocutils.geom.point.Point.from_xyz(10, -5, 0)
    assert p1.middle(p2).x == 5
    assert p1.middle(p2).y == -2.5
    assert p1.middle(p2).z == 0


def test_point_translate():
    p1 = aocutils.geom.point.Point.from_xyz(10, 2.56, 4)
    v = aocutils.geom.vector.Vector.from_tuple((10, -5, 0.0))
    assert p1.translate(v).x == 20
    assert p1.translate(v).y == -2.44
    assert p1.translate(v).z == 4


def test_vector_norm():
    v = aocutils.geom.vector.Vector.from_xyz(0, 0, 0)
    assert v.norm == 0

    v = aocutils.geom.vector.Vector.from_xyz(3, 4, 0)
    assert v.norm == 5


def test_perpendicular_vector():
    v1 = aocutils.geom.vector.Vector.from_xyz(1, 0, 0)
    v2 = aocutils.geom.vector.Vector.from_xyz(0, 1, 0)

    assert v1.perpendicular(v2).norm == 1
    assert v1.perpendicular(v2).x == 0
    assert v1.perpendicular(v2).y == 0
    assert v1.perpendicular(v2).z == 1


def test_multiply_vector():
    v1 = aocutils.geom.vector.Vector.from_xyz(10, 10, 0)
    v1 *= 2

    assert v1.x == 20
    assert v1.y == 20
    assert v1.z == 0


def test_divide_vector():
    v1 = aocutils.geom.vector.Vector.from_xyz(10, 10, 0)
    v1 /= 2

    assert v1.x == 5
    assert v1.y == 5
    assert v1.z == 0

def test_divide_vector_by_norm():
    v1 = aocutils.geom.vector.Vector.from_xyz(10, 10, 0)
    v1 /= v1.norm

    assert v1.norm - 1e-5 <= v1.norm <= v1.norm + 1e-5

