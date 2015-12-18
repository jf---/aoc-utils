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

PY3 = not (int(sys.version.split('.')[0]) <= 2)

@pytest.fixture()
def box_shape():
    r"""Box shape for testing"""
    return OCC.BRepPrimAPI.BRepPrimAPI_MakeBox(10, 20, 30).Shape()

def test_curve(box_shape):
    t = aocutils.topology.Topo(box_shape)
    wire = t.wires().__next__() if PY3 else t.wires().next()

    curve = aocutils.brep.wire.Wire(wire).to_curve()
    assert isinstance(curve, OCC.Geom.Geom_BSplineCurve)
    assert issubclass(curve.__class__, OCC.Geom.Geom_Curve)

    bspline = aocutils.geom.curve.Curve(curve).to_bspline()
    assert isinstance(bspline, OCC.Geom.Handle_Geom_BSplineCurve)
    assert isinstance(bspline.GetObject(), OCC.Geom.Geom_BSplineCurve)
