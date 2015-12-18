#!/usr/bin/python
# coding: utf-8

r"""tests/test_brep.py
"""


import sys
import pytest

import OCC.BRepPrimAPI
import OCC.Geom
import OCC.gp
import OCC.TopAbs
import OCC.Adaptor3d
import OCC.GeomLProp

import aocutils.topology
import aocutils.tolerance
import aocutils.brep.vertex
import aocutils.brep.edge
import aocutils.brep.solid
import aocutils.brep.shell
import aocutils.brep.wire
import aocutils.brep.face
import aocutils.brep.base


PY3 = not (int(sys.version.split('.')[0]) <= 2)


@pytest.fixture()
def box_shape():
    r"""Box shape for testing"""
    return OCC.BRepPrimAPI.BRepPrimAPI_MakeBox(10, 20, 30).Shape()


@pytest.fixture()
def sphere_shape():
    r"""Box shape for testing"""
    return OCC.BRepPrimAPI.BRepPrimAPI_MakeSphere(10).Shape()

def test_base(box_shape):
    r"""Test Base class in brep/base.py"""
    b = aocutils.brep.base.BaseObject(box_shape, name="box_shape")
    assert b.wrapped_instance is not None
    assert b.name == "box_shape"
    assert b.topo_type == "solid"
    assert b.is_valid is True
    assert b.orientation == OCC.TopAbs.TopAbs_FORWARD


def test_edge_line(box_shape):
    t = aocutils.topology.Topo(box_shape)  # wrap the box in a Topo object
    edge_0 = t.edges().__next__() if PY3 else t.edges().next()  # take the first edge, it's a TopoDS_Edge
    assert not edge_0.IsNull()
    my_edge = aocutils.brep.edge.Edge(edge_0)  # create an Edge
    assert my_edge.tolerance == 1e-06

    assert my_edge.length() == 30.
    assert my_edge.domain == (0., 30.)
    assert my_edge.is_valid is True
    assert my_edge.is_closed is False
    assert my_edge.is_periodic is False
    assert my_edge.is_rational is False
    assert my_edge.continuity == "GeomAbs_CN"
    assert my_edge.degree == 1
    assert my_edge.nb_knots == -1  # TODO : check that these properties return someting meaningful for other curve types
    assert my_edge.nb_poles == -1
    assert issubclass(my_edge.curve.__class__, OCC.Geom.Geom_Curve)
    assert my_edge.curve_handle is not None
    assert my_edge.geom_curve_handle is not None
    assert my_edge.geom_type == 'line'
    with pytest.raises(RuntimeError):
        assert my_edge.radius(1.) is not None
    assert my_edge.curvature(1.) == 0.
    assert my_edge.tangent(1.) is not None
    with pytest.raises(ValueError):
        assert my_edge.normal(1.) is not None
    assert my_edge.derivative(1., 1) is not None
    assert my_edge.derivative(1., 2) is not None
    assert my_edge.derivative(1., 3) is not None
    assert isinstance(my_edge.derivative(1., 1), OCC.gp.gp_Vec)
    assert isinstance(my_edge.derivative(19., 2), OCC.gp.gp_Vec)
    assert isinstance(my_edge.derivative(10., 3), OCC.gp.gp_Vec)


def test_edge_sphere(sphere_shape):
    t = aocutils.topology.Topo(sphere_shape, return_iter=False)
    edge_1 = t.edges()[1]
    assert not edge_1.IsNull()
    my_edge = aocutils.brep.edge.Edge(edge_1)  # create an Edge
    assert my_edge.tolerance == 1e-06

    assert my_edge.length() > 0.
    print(my_edge.domain[0])
    print(my_edge.domain[1])
    assert my_edge.domain[1] > my_edge.domain[0]
    assert my_edge.is_valid is True
    assert my_edge.is_closed is False
    assert my_edge.is_periodic is False
    assert my_edge.is_rational is False
    assert my_edge.continuity == "GeomAbs_CN"
    assert my_edge.geom_type == 'circle'
    assert my_edge.degree == 2
    assert my_edge.nb_knots == -1  # TODO : check that these properties return someting meaningful for other curve types
    assert my_edge.nb_poles == -1
    assert issubclass(my_edge.curve.__class__, OCC.Geom.Geom_Curve)
    assert my_edge.curve_handle is not None
    assert my_edge.geom_curve_handle is not None

    assert my_edge.radius(6.).X() < my_edge.tolerance
    assert my_edge.radius(6.).Y() < my_edge.tolerance
    assert my_edge.radius(6.).Z() < my_edge.tolerance
    assert 1/10. - my_edge.tolerance <= my_edge.curvature(6.) <= 1/10. + my_edge.tolerance
    assert my_edge.tangent(6.) is not None
    assert my_edge.normal(6.) is not None
    assert my_edge.derivative(1., 1) is not None
    assert my_edge.derivative(1., 2) is not None
    assert my_edge.derivative(1., 3) is not None
    assert isinstance(my_edge.derivative(1., 1), OCC.gp.gp_Vec)
    assert isinstance(my_edge.derivative(19., 2), OCC.gp.gp_Vec)
    assert isinstance(my_edge.derivative(10., 3), OCC.gp.gp_Vec)


def test_face_flat(box_shape):
    t = aocutils.topology.Topo(box_shape)  # wrap the box in a Topo object
    face_0 = t.faces().__next__() if PY3 else t.faces().next()
    assert not face_0.IsNull()
    my_face = aocutils.brep.face.Face(face_0)
    assert my_face.tolerance == 1e-06
    assert my_face.is_u_periodic is False
    assert my_face.is_v_periodic is False
    assert my_face.is_u_closed is False
    assert my_face.is_v_closed is False
    assert my_face.is_u_rational is False
    assert my_face.is_v_rational is False
    assert my_face.u_continuity == "GeomAbs_CN"
    assert my_face.v_continuity == "GeomAbs_CN"
    domain = my_face.domain
    assert len(domain) == 4
    assert domain[1] > domain[0]
    assert domain[3] > domain[2]
    assert isinstance(my_face.midpoint, OCC.gp.gp_Pnt)
    assert isinstance(my_face.midpoint_parameters, tuple)
    assert my_face.topo is not None
    assert issubclass(my_face.surface.__class__, OCC.Geom.Geom_Surface)
    assert my_face.surface_handle is not None
    assert my_face.adaptor is not None
    assert my_face.adaptor_handle is not None
    assert my_face.is_closed == (False, False)
    assert my_face.is_planar() == True
    assert my_face.is_plane
    assert my_face.is_trimmed
    # todo : test for on_trimmed
    pnt = my_face.parameter_to_point(1., 1.)
    assert isinstance(pnt, OCC.gp.gp_Pnt)
    assert my_face.point_to_parameter(pnt) == (1., 1.)
    # todo : test continuity_edge_face
    # todo : test project_vertex
    # todo : test project_curve
    # todo : test project_edge
    assert isinstance(my_face.iso_curve('u', 1.), OCC.Adaptor3d.Adaptor3d_IsoCurve)
    assert len(my_face.edges) == 4
    assert isinstance(my_face.local_props(1., 1.), OCC.GeomLProp.GeomLProp_SLProps)
    assert my_face.gaussian_curvature(1., 1.) == 0.
    assert my_face.min_curvature(1., 1.) == 0.
    assert my_face.mean_curvature(1., 1.) == 0.
    assert my_face.max_curvature(1., 1.) == 0.
    assert isinstance(my_face.normal(1., 1.), OCC.gp.gp_Vec)
    assert isinstance(my_face.tangent(1., 1.), tuple)
    assert isinstance(my_face.tangent(1., 1.)[0], OCC.gp.gp_Vec)
    assert isinstance(my_face.tangent(1., 1.)[1], OCC.gp.gp_Vec)
    assert my_face.radius(1., 1.) == float('inf')
    assert my_face.geom_type == 'plane'


def test_wire(box_shape):
    # take the first edge
    t = aocutils.topology.Topo(box_shape)
    wire = t.wires().__next__() if PY3 else t.wires().next()
    my_wire = aocutils.brep.wire.Wire(wire)
    assert my_wire.tolerance == 1e-06

    curve = aocutils.brep.wire.Wire(wire).to_curve()
    assert isinstance(curve, OCC.Geom.Geom_BSplineCurve)
    assert issubclass(curve.__class__, OCC.Geom.Geom_Curve)


def test_vertex(box_shape):
    my_vertex = aocutils.brep.vertex.Vertex(1., 2., -2.6)
    assert my_vertex.tolerance == 1e-06
    assert my_vertex.x == 1.
    assert my_vertex.y == 2.
    assert my_vertex.z == -2.6

    vertices = aocutils.topology.Topo(box_shape).vertices()
    for vert in vertices:
        assert isinstance(aocutils.brep.vertex.Vertex.to_pnt(vert), OCC.gp.gp_Pnt)


def test_shell():
    my_shell = aocutils.brep.shell.Shell(OCC.BRepPrimAPI.BRepPrimAPI_MakeBox(10, 20, 30).Shell())
    assert my_shell.tolerance == 1e-06


def test_solid():
    my_solid = aocutils.brep.solid.Solid(OCC.BRepPrimAPI.BRepPrimAPI_MakeBox(10, 20, 30).Solid())
    assert my_solid.tolerance == 1e-06
