#!/usr/bin/python
# coding: utf-8

r"""analyze package tests"""

import pytest

import OCC.gp
import OCC.TopAbs

import aocutils.primitives
import aocutils.tolerance
import aocutils.topology
import aocutils.mesh
import aocutils.exceptions
import aocutils.brep.edge_make
import aocutils.brep.wire_make
import aocutils.brep.face_make


import aocutils.analyze.bounds
import aocutils.analyze.distance
import aocutils.analyze.global_
import aocutils.analyze.inclusion


box = aocutils.primitives.box(10, 20, 30)
sphere = aocutils.primitives.sphere(10)
sphere_2 = aocutils.primitives.sphere(OCC.gp.gp_Pnt(40, 0, 0), 10)
edge = aocutils.brep.edge_make.line(OCC.gp.gp_Pnt(0, 0, 0), OCC.gp.gp_Pnt(20, 0, 0))
edge_2 = aocutils.brep.edge_make.line(OCC.gp.gp_Pnt(20, 0, 0), OCC.gp.gp_Pnt(20, 20, 0))
edge_3 = aocutils.brep.edge_make.line(OCC.gp.gp_Pnt(20, 20, 0), OCC.gp.gp_Pnt(0, 20, 0))
edge_4 = aocutils.brep.edge_make.line(OCC.gp.gp_Pnt(0, 20, 0), OCC.gp.gp_Pnt(0, 0, 0))
wire = aocutils.brep.wire_make.wire([edge, edge_2])
closed_wire = aocutils.brep.wire_make.wire([edge, edge_2, edge_3, edge_4])
face = aocutils.brep.face_make.face(closed_wire)
tol = aocutils.tolerance.OCCUTILS_DEFAULT_TOLERANCE


def test_bounds_box():
    # occutils.mesh.mesh(box)
    bb = aocutils.analyze.bounds.BoundingBox(box)
    assert 10 <= bb.x_span < 10 + 2.001 * tol
    assert 20 <= bb.y_span < 20 + 2.001 * tol
    assert 30 <= bb.z_span < 30 + 2.001 * tol


def test_bounds_sphere():
    # occutils.mesh.mesh(box)
    bb = aocutils.analyze.bounds.BoundingBox(sphere)
    assert 20 <= bb.x_span < 20 + 2.001 * tol
    assert 20 <= bb.y_span < 20 + 2.001 * tol
    assert 20 <= bb.z_span < 20 + 2.001 * tol


def test_bounds_sphere_boundingbox_middle():
    # occutils.mesh.mesh(box)
    bb = aocutils.analyze.bounds.BoundingBox(sphere)
    assert bb.centre.X() < tol / 10.
    assert bb.centre.Y() < tol / 10.
    assert bb.centre.Z() < tol / 10.


def test_minimum_distance():
    md = aocutils.analyze.distance.MinimumDistance(sphere, sphere_2)
    assert md.minimum_distance == 20.
    assert md.nb_solutions == 1
    assert type(md.point_pairs[0][0]) == OCC.gp.gp_Pnt


def test_face():
    import aocutils.brep.face
    # box face is planar
    face = aocutils.brep.face.Face(aocutils.topology.Topo(box, return_iter=False).faces[0])
    assert face.is_plane is True
    assert face.gaussian_curvature(0.1, 0.1) == 0.0
    assert face.mean_curvature(0.1, 0.1) == 0.0
    assert face.min_curvature(0.1, 0.1) == 0.0
    assert face.max_curvature(0.1, 0.1) == 0.0

    # sphere face is not planar
    face = aocutils.brep.face.Face(aocutils.topology.Topo(sphere, return_iter=False).faces[0])
    assert face.is_plane is False
    assert face.orientation == OCC.TopAbs.TopAbs_FORWARD
    assert -1 / 10. - tol < face.mean_curvature(0.1, 0.1) <= -1 / 10. + tol  # todo : how is curvature sign determined
    assert -1 / 10. - tol < face.min_curvature(0.1, 0.1) <= -1 / 10. + tol
    assert -1 / 10. - tol < face.max_curvature(0.1, 0.1) <= -1 / 10. + tol
    assert 1 / 10.**2 - tol < face.gaussian_curvature(0.1, 0.1) <= 1 / 10.**2 + tol


def test_global_properties():
    box_properties = aocutils.analyze.global_.GlobalProperties(box)
    assert box_properties.volume() == 10 * 20 * 30

    box_shell = aocutils.topology.Topo(box, return_iter=False).shells[0]
    shell_properties = aocutils.analyze.global_.GlobalProperties(box_shell)
    assert 2200 - tol <= shell_properties.area() <= 2200 + tol

    edge_properties = aocutils.analyze.global_.GlobalProperties(edge)
    assert edge_properties.length() == 20

    with pytest.raises(aocutils.exceptions.WrongTopologicalType):
        edge_properties.volume()

    with pytest.raises(aocutils.exceptions.WrongTopologicalType):
        box_properties.area()

    with pytest.raises(aocutils.exceptions.WrongTopologicalType):
        box_properties.length()

    with pytest.raises(aocutils.exceptions.WrongTopologicalType):
        shell_properties.length()

    with pytest.raises(aocutils.exceptions.WrongTopologicalType):
        shell_properties.volume()

    edge_centre = edge_properties.centre()
    assert type(edge_centre) == OCC.gp.gp_Pnt
    assert edge_centre.X() == 10
    assert edge_centre.Y() == 0
    assert edge_centre.Z() == 0

    sphere_properties = aocutils.analyze.global_.GlobalProperties(sphere)
    sphere_centre = sphere_properties.centre()
    assert - tol < sphere_centre.X() < tol
    assert - tol < sphere_centre.Y() < tol
    assert - tol < sphere_centre.Z() < tol

    wire_properties = aocutils.analyze.global_.GlobalProperties(wire)
    assert wire_properties.length() == 40


def test_inclusion():
    assert aocutils.analyze.inclusion.point_in_boundingbox(sphere, OCC.gp.gp_Pnt(9, 9, 9)) == True

    assert aocutils.analyze.inclusion.point_in_solid(sphere, OCC.gp.gp_Pnt(9, 0, 0)) == True
    assert aocutils.analyze.inclusion.point_in_solid(sphere, OCC.gp.gp_Pnt(9, 9, 9)) == False
    assert aocutils.analyze.inclusion.point_in_solid(sphere, OCC.gp.gp_Pnt(10, 0, 0)) == None

    with pytest.raises(aocutils.exceptions.WrongTopologicalType):
        aocutils.analyze.inclusion.point_in_solid(edge, OCC.gp.gp_Pnt(10, 0, 0))

    with pytest.raises(aocutils.exceptions.WrongTopologicalType):
        aocutils.analyze.inclusion.point_in_solid(aocutils.topology.Topo(sphere, return_iter=False).faces[0],
                                                  OCC.gp.gp_Pnt(10, 0, 0))

    sphere_shell = aocutils.topology.Topo(sphere, return_iter=False).shells[0]
    assert aocutils.analyze.inclusion.point_in_boundingbox(sphere_shell, OCC.gp.gp_Pnt(9, 9, 9)) == True
    assert aocutils.analyze.inclusion.point_in_solid(sphere_shell, OCC.gp.gp_Pnt(9, 0, 0)) == True
    assert aocutils.analyze.inclusion.point_in_solid(sphere_shell, OCC.gp.gp_Pnt(9, 9, 9)) == False
    assert aocutils.analyze.inclusion.point_in_solid(sphere_shell, OCC.gp.gp_Pnt(10, 0, 0)) == None
