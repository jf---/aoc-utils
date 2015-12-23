#!/usr/bin/python
# coding: utf-8

r"""
"""

import pytest

import OCC.BRepPrimAPI
import OCC.TopoDS

import aocutils.fixes
import aocutils.topology


@pytest.fixture()
def box_shape():
    r"""Box shape for testing as a pytest fixture"""
    return OCC.BRepPrimAPI.BRepPrimAPI_MakeBox(10, 20, 30).Shape()


def test_fix_shape(box_shape):
    r"""test shape fixing

    Parameters
    ----------
    box_shape : TopoDS_Shape
        Box shape (pytest fixture)

    """
    # check the result of fixing a shape is a shape
    assert isinstance(aocutils.fixes.fix_shape(box_shape), OCC.TopoDS.TopoDS_Shape)


def test_fix_face(box_shape):
    r"""test face fixing

    Parameters
    ----------
    box_shape : TopoDS_Shape
        Box shape (pytest fixture)

    """
    # get a face
    face = aocutils.topology.Topo(box_shape, return_iter=False).faces[0]

    # check the fixing result is a TopoDS_Face
    assert isinstance(aocutils.fixes.fix_face(face), OCC.TopoDS.TopoDS_Face)


def test_fix_tolerance(box_shape):
    r"""test tolerance fixing

    Parameters
    ----------
    box_shape : TopoDS_Shape
        Box shape (pytest fixture)

    """
    aocutils.fixes.fix_tolerance(box_shape)
    assert True


def test_fix_continuity(box_shape):
    r"""test continuity fixing

    Parameters
    ----------
    box_shape : TopoDS_Shape
        Box shape (pytest fixture)

    """
    # get an edge
    edge = aocutils.topology.Topo(box_shape, return_iter=False).edges[0]

    # test types
    assert isinstance(aocutils.fixes.fix_continuity(edge), OCC.TopoDS.TopoDS_Shape)
    assert not isinstance(aocutils.fixes.fix_continuity(edge), OCC.TopoDS.TopoDS_Edge)
    assert not aocutils.fixes.fix_continuity(edge).IsNull()

# TODO : test curve resampling
