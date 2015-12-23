#!/usr/bin/python
# coding: utf-8

r"""types module tests"""

import pytest
import logging

import OCC.BRepPrimAPI
import OCC.TopAbs

import aocutils.topology
import aocutils.types

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s :: %(levelname)6s :: %(module)20s :: %(lineno)3d :: %(message)s')

box_x_dim = 10.
box_y_dim = 20.
box_z_dim = 30.


@pytest.fixture()
def box_shape():
    r"""Box shape for testing as a pytest fixture"""
    return OCC.BRepPrimAPI.BRepPrimAPI_MakeBox(box_x_dim, box_y_dim, box_z_dim).Shape()


sphere_radius = 10


@pytest.fixture()
def sphere_shape():
    r"""Sphere shape for testing as a pytext fixture"""
    return OCC.BRepPrimAPI.BRepPrimAPI_MakeSphere(sphere_radius).Shape()


def test_bidir_dict():
    r"""Test BidirDict"""

    # all values are unique
    d = {"a": 1, "b": 2, "c": 3}
    bd = aocutils.types.BidirDict(d)
    assert bd["a"] == 1
    assert bd[1] == "a"

    # duplicate a value
    d = {"a": 1, "b": 2, "c": 3, "d": 1}
    bd = aocutils.types.BidirDict(d)
    with pytest.raises(KeyError):
        _ = bd["a"]


def test_look_up_table():
    r"""Test look up tables"""
    assert aocutils.types.topo_lut[OCC.TopAbs.TopAbs_SOLID] == "solid"
    with pytest.raises(KeyError):
        _ = aocutils.types.topo_lut[111]

# def test_classes():
#     assert aocutils.types.classes == ['BidirDict', 'OCC', 'PY3', '__builtins__', '__doc__', '__file__', '__name__',
#                                       '__package__', 'aocutils', 'brep_check_dict', 'brepcheck_lut', 'curve_lut',
#                                       'curve_types_dict', 'geom_lut', 'geom_types_dict', 'itertools', 'logger',
#                                      'logging', 'orient_dict', 'orient_lut', 'state_dict', 'state_lut', 'surface_lut',
#                                       'surface_types_dict', 'sys', 'topo_lut', 'topo_types_dict']
#
#
# def test_geom_classes():
#
#     assert aocutils.types.geom_classes == []
#
#
# def test_what_is_face(box_shape):
#     r"""test the what_is_face function"""
#
#     # wrap the box shape in a Topo object
#     topo = aocutils.topology.Topo(box_shape, return_iter=False)
#
#     # get the first face
#     face = topo.faces()[0]
#
#     assert aocutils.types.what_is_face(face) == []
