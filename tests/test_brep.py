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


def test_base(box_shape):
    r"""Test Base class in brep/base.py"""
    b = aocutils.brep.base.BaseObject(box_shape, name="box_shape")
    assert b.wrapped_instance is not None
    assert b.name == "box_shape"
    assert b.topo_type == "solid"
    assert b.is_valid is True
    assert b.orientation == OCC.TopAbs.TopAbs_FORWARD


def test_edge_line(box_shape):
    r"""aocutils straight Edge test

    Parameters
    ----------
    box_shape : TopoDS_Shape
        Box shape (pytest fixture)

    """
    # wrap the box in a Topo object
    topo = aocutils.topology.Topo(box_shape)

    # take the first edge, it's a TopoDS_Edge
    edge_0 = topo.edges().__next__() if PY3 else topo.edges().next()
    assert not edge_0.IsNull()

    # create an aocutils Edge
    my_edge = aocutils.brep.edge.Edge(edge_0)

    # check the aocutils Edge
    assert my_edge.tolerance == 1e-06
    assert my_edge.length() == box_z_dim
    assert my_edge.domain == (0., box_z_dim)

    domain_start = my_edge.domain[0]
    domain_end = my_edge.domain[1]
    domain_middle = (domain_start + domain_end) / 2.

    assert my_edge.is_valid is True
    assert my_edge.is_closed is False
    assert my_edge.is_periodic is False
    assert my_edge.is_rational is False
    assert my_edge.continuity == "GeomAbs_CN"
    assert my_edge.degree == 1
    assert my_edge.nb_knots == -1  # TODO: check that these properties return something meaningful for other curve types
    assert my_edge.nb_poles == -1
    assert my_edge.curve_handle is not None
    assert my_edge.geom_curve_handle is not None
    assert my_edge.geom_type == 'line'
    assert my_edge.curvature(domain_middle) == 0.
    assert my_edge.tangent(domain_middle) is not None

    # Check property types
    assert issubclass(my_edge.curve.__class__, OCC.Geom.Geom_Curve)
    assert isinstance(my_edge.derivative(domain_middle, 1), OCC.gp.gp_Vec)
    assert isinstance(my_edge.derivative(domain_middle, 2), OCC.gp.gp_Vec)
    assert isinstance(my_edge.derivative(domain_middle, 3), OCC.gp.gp_Vec)

    # TODO : RuntimeError in one case, ValueError in the other !
    with pytest.raises(RuntimeError):
        assert my_edge.radius(1.) is not None
    with pytest.raises(ValueError):
        assert my_edge.normal(1.) is not None


def test_edge_sphere(sphere_shape):
    r"""aocutils curved Edge test

    Parameters
    ----------
    sphere_shape : TopoDS_Shape
        Sphere shape (pytest fixture)

    """
    # wrap the sphere in a Topo object
    topo = aocutils.topology.Topo(sphere_shape, return_iter=False)

    # take the first edge, it's a TopoDS_Edge
    edge_1 = topo.edges()[1]
    assert not edge_1.IsNull()

    # create an aocutils Edge
    my_edge = aocutils.brep.edge.Edge(edge_1)  # create an Edge
    assert my_edge.tolerance == 1e-06

    # check the aocutils Edge
    assert my_edge.length() > 0.
    assert my_edge.domain[1] > my_edge.domain[0]

    domain_start = my_edge.domain[0]
    domain_end = my_edge.domain[1]
    domain_middle = (domain_start + domain_end) / 2.

    assert my_edge.is_valid is True
    assert my_edge.is_closed is False
    assert my_edge.is_periodic is False
    assert my_edge.is_rational is False
    assert my_edge.continuity == "GeomAbs_CN"
    assert my_edge.geom_type == 'circle'
    assert my_edge.degree == 2
    assert my_edge.nb_knots == -1  # TODO : check that these properties return someting meaningful for other curve types
    assert my_edge.nb_poles == -1
    assert my_edge.curve_handle is not None
    assert my_edge.geom_curve_handle is not None

    # check the curvature is 1 / radius (r=10)
    curvature = 1. / sphere_radius
    assert curvature - 1e-6 <= my_edge.curvature(domain_middle) <= curvature + 1e6

    # Check that the computed centre of curvature is at the origin
    assert my_edge.radius(domain_middle).X() < my_edge.tolerance
    assert my_edge.radius(domain_middle).Y() < my_edge.tolerance
    assert my_edge.radius(domain_middle).Z() < my_edge.tolerance

    # Check property types
    assert isinstance(my_edge.tangent(domain_middle), OCC.gp.gp_Dir)
    assert isinstance(my_edge.normal(domain_middle), OCC.gp.gp_Dir)
    assert issubclass(my_edge.curve.__class__, OCC.Geom.Geom_Curve)
    assert isinstance(my_edge.derivative(domain_start, 1), OCC.gp.gp_Vec)
    assert isinstance(my_edge.derivative(domain_middle, 2), OCC.gp.gp_Vec)
    assert isinstance(my_edge.derivative(domain_end, 3), OCC.gp.gp_Vec)

    # TODO: radius and normal outside of domain


def test_face_flat(box_shape):
    r"""aocutils flat Face test

    Parameters
    ----------
    box_shape : TopoDS_Shape
        Box shape (pytest fixture)

    """
    # wrap the box in a Topo object
    t = aocutils.topology.Topo(box_shape)  # wrap the box in a Topo object

    # take the first face, it is a TopoDS_Face
    face_0 = t.faces().__next__() if PY3 else t.faces().next()
    assert not face_0.IsNull()

    # create an aocutils Face
    my_face = aocutils.brep.face.Face(face_0)

    # check the aocutils Face
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
    assert domain[1] > domain[0]  # u max > u min
    assert domain[3] > domain[2]  # v max > v min

    u_domain_start = domain[0]
    u_domain_end = domain[1]
    u_domain_middle = (u_domain_start + u_domain_end) / 2.
    v_domain_start = domain[2]
    v_domain_end = domain[3]
    v_domain_middle = (v_domain_start + v_domain_end) / 2.

    assert my_face.topo is not None
    assert my_face.surface_handle is not None
    assert my_face.adaptor is not None
    assert my_face.adaptor_handle is not None
    assert my_face.is_closed == (False, False)
    assert my_face.is_planar() == True
    assert my_face.is_plane
    assert my_face.is_trimmed
    # todo : test for on_trimmed

    # create point from u, v parameters
    pnt = my_face.parameter_to_point(u_domain_middle, v_domain_middle)
    # check that the parameters at the created point are the same as the one used to create the point
    assert my_face.point_to_parameter(pnt) == (u_domain_middle, v_domain_middle)

    # todo : test continuity_edge_face
    # todo : test project_vertex
    # todo : test project_curve
    # todo : test project_edge

    assert len(my_face.edges) == 4
    assert my_face.gaussian_curvature(u_domain_middle, v_domain_middle) == 0.
    assert my_face.min_curvature(u_domain_middle, v_domain_middle) == 0.
    assert my_face.mean_curvature(u_domain_middle, v_domain_middle) == 0.
    assert my_face.max_curvature(u_domain_middle, v_domain_middle) == 0.

    assert my_face.radius(u_domain_middle, v_domain_middle) == float('inf')
    assert my_face.geom_type == 'plane'

    # check property types
    assert isinstance(my_face.midpoint, OCC.gp.gp_Pnt)
    assert isinstance(my_face.midpoint_parameters, tuple)
    assert issubclass(my_face.surface.__class__, OCC.Geom.Geom_Surface)
    assert isinstance(pnt, OCC.gp.gp_Pnt)
    assert isinstance(my_face.iso_curve('u', u_domain_middle), OCC.Adaptor3d.Adaptor3d_IsoCurve)
    assert isinstance(my_face.local_props(u_domain_middle, v_domain_middle), OCC.GeomLProp.GeomLProp_SLProps)
    assert isinstance(my_face.normal(u_domain_middle, v_domain_middle), OCC.gp.gp_Vec)
    assert isinstance(my_face.tangent(u_domain_middle, v_domain_middle), tuple)
    assert isinstance(my_face.tangent(u_domain_middle, v_domain_middle)[0], OCC.gp.gp_Vec)
    assert isinstance(my_face.tangent(u_domain_middle, v_domain_middle)[1], OCC.gp.gp_Vec)


def test_wire(box_shape):
    r"""aocutils Wire test

    Parameters
    ----------
    box_shape : TopoDS_Shape
        Box shape (pytest fixture)

    """
    # wrap the box in a Topo object
    t = aocutils.topology.Topo(box_shape)

    # take the first wire
    wire = t.wires().__next__() if PY3 else t.wires().next()

    # create the aocutils Wire
    my_wire = aocutils.brep.wire.Wire(wire)

    # check the aocutils Wire
    assert my_wire.tolerance == 1e-06

    curve = aocutils.brep.wire.Wire(wire).to_curve()
    assert isinstance(curve, OCC.Geom.Geom_BSplineCurve)
    assert issubclass(curve.__class__, OCC.Geom.Geom_Curve)


def test_vertex(box_shape):
    r"""aocutils Vertex test

    Parameters
    ----------
    box_shape : TopoDS_Shape
        Box shape (pytest fixture)

    """
    # create the Vertex
    my_vertex = aocutils.brep.vertex.Vertex(1., 2., -2.6)

    # check the aocutils Vertex
    assert my_vertex.tolerance == 1e-06
    assert my_vertex.x == 1.
    assert my_vertex.y == 2.
    assert my_vertex.z == -2.6

    vertices = aocutils.topology.Topo(box_shape).vertices()
    for vert in vertices:
        assert isinstance(aocutils.brep.vertex.Vertex.to_pnt(vert), OCC.gp.gp_Pnt)


def test_shell(box_shape):
    r"""aocutils Shell test

    Parameters
    ----------
    box_shape : TopoDS_Shape
        Box shape (pytest fixture)

    """
    # create the aocutils Shell
    my_shell = aocutils.brep.shell.Shell(OCC.BRepPrimAPI.BRepPrimAPI_MakeBox(box_x_dim, box_y_dim, box_z_dim).Shell())

    # check the aocutils Shell
    assert my_shell.tolerance == 1e-06


def test_solid(box_shape):
    r"""aocutils Solid test

    Parameters
    ----------
    box_shape : TopoDS_Shape
        Box shape (pytest fixture)

    """
    # create the aocutils Solid
    my_solid = aocutils.brep.solid.Solid(OCC.BRepPrimAPI.BRepPrimAPI_MakeBox(box_x_dim, box_y_dim, box_z_dim).Solid())

    # check the aocutils Solid
    assert my_solid.tolerance == 1e-06
