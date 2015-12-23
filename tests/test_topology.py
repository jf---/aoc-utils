#!/usr/bin/python
# coding: utf-8

r"""topology module tests"""

import sys
import pytest

import OCC.BRepPrimAPI
import OCC.TopoDS

import aocutils.topology
import aocutils.primitives
import aocutils.brep.edge
import aocutils.brep.face
import aocutils.brep.wire
import aocutils.brep.vertex
import aocutils.brep.shell
import aocutils.brep.solid

PY3 = not (int(sys.version.split('.')[0]) <= 2)


@pytest.fixture()
def box_shape():
    r"""Box shape for testing as a pytest fixture"""
    return OCC.BRepPrimAPI.BRepPrimAPI_MakeBox(10, 20, 30).Shape()
#
# @pytest.fixture()
# def sphere_shape():
#     r"""Sphere shape of radius 10 for testing"""
#     return OCC.BRepPrimAPI.BRepPrimAPI_MakeSphere(10.).Shape()


@pytest.fixture()
def topo():
    r"""Topo object testing as a pytest fixture"""
    # we use return_iter=True as the original tests were written with a Topo did not have the option to return lists
    # instead of iterators
    return aocutils.topology.Topo(aocutils.primitives.box(10, 10, 10), return_iter=True)


def test_shape_to_topology(box_shape):
    r"""test shape_to_topology

    Parameters
    ----------
    box_shape : TopoDS_Shape
        Box shape (pytest fixture)

    """

    assert isinstance(aocutils.topology.shape_to_topology(box_shape), OCC.TopoDS.TopoDS_Solid)
    assert isinstance(aocutils.topology.shape_to_topology(box_shape), OCC.TopoDS.TopoDS_Shape)

    assert not isinstance(box_shape, OCC.TopoDS.TopoDS_Solid)
    assert not isinstance(aocutils.topology.shape_to_topology(box_shape), OCC.TopoDS.TopoDS_Compound)
    assert not isinstance(aocutils.topology.shape_to_topology(box_shape), OCC.TopoDS.TopoDS_CompSolid)
    assert not isinstance(aocutils.topology.shape_to_topology(box_shape), OCC.TopoDS.TopoDS_Shell)
    assert not isinstance(aocutils.topology.shape_to_topology(box_shape), OCC.TopoDS.TopoDS_Face)

    assert issubclass(aocutils.topology.shape_to_topology(box_shape).__class__, OCC.TopoDS.TopoDS_Shape)


def test_wrap_subclass_of_topodsshape(topo):
    r"""Test the wrapping of a TopoDS_Shape subclass in a Topo object

    Parameters
    ----------
    topo : aocutils.topology.Topo
        Topo object (pytest fixture)

    """
    shell = list(topo.shells)[0]
    assert isinstance(shell, OCC.TopoDS.TopoDS_Shell)
    new_topo = aocutils.topology.Topo(shell)
    assert new_topo.number_of_faces == 6


def test_loop_faces(topo):
    r"""Make sure there are 6 faces in a box

    Parameters
    ----------
    topo : aocutils.topology.Topo
        Topo object (pytest fixture)

    """
    i = 0
    for face in topo.faces:
        i += 1
        assert(isinstance(face, OCC.TopoDS.TopoDS_Face))
    assert i == 6


def test_loop_edges(topo):
    r"""Make sure there are 12 edges in a box

    Parameters
    ----------
    topo : aocutils.topology.Topo
        Topo object (pytest fixture)

    """
    i = 0
    for face in topo.edges:
        i += 1
        assert(isinstance(face, OCC.TopoDS.TopoDS_Edge))
    assert i == 12


def test_number_of_topological_entities(topo):
    r"""Test the number of entities for a box

    Parameters
    ----------
    topo : aocutils.topology.Topo
        Topo object (pytest fixture)

    """
    assert topo.number_of_faces == 6
    assert topo.number_of_edges == 12
    assert topo.number_of_vertices == 8
    assert topo.number_of_wires == 6
    assert topo.number_of_solids == 1
    assert topo.number_of_shells == 1
    assert topo.number_of_compounds == 0
    assert topo.number_of_comp_solids == 0


def test_nested_iteration(topo):
    """check nested looping

    Parameters
    ----------
    topo : aocutils.topology.Topo
        Topo object (pytest fixture)

    """
    for f in topo.faces:
        for e in topo.edges:
            assert isinstance(f, OCC.TopoDS.TopoDS_Face)
            assert isinstance(e, OCC.TopoDS.TopoDS_Edge)


def test_kept_reference(topo):
    """did we keep a reference after looping several time through a list
    of topological entities?

    Parameters
    ----------
    topo : aocutils.topology.Topo
        Topo object (pytest fixture)

    """
    _tmp = list()
    _faces = [i for i in topo.faces]
    for f in _faces:
        _tmp.append(0 == f.IsNull())
    for f in _faces:
        _tmp.append(0 == f.IsNull())
    assert all(_tmp)


def test_edge_face(topo):
    r"""

    Parameters
    ----------
    topo : aocutils.topology.Topo
        Topo object (pytest fixture)

    """
    edg = topo.edges.__next__() if PY3 else topo.edges.next()
    face = topo.faces.__next__() if PY3 else topo.faces.next()

    faces_from_edge = [i for i in topo.faces_from_edge(edg)]
    assert (len(faces_from_edge) == topo.number_of_faces_from_edge(edg))

    edges_from_face = [i for i in topo.edges_from_face(face)]
    assert (len(edges_from_face) == topo.number_of_edges_from_face(face))


def test_edge_wire(topo):
    r"""

    Parameters
    ----------
    topo : aocutils.topology.Topo
        Topo object (pytest fixture)

    """
    edg = topo.edges.__next__() if PY3 else topo.edges.next()
    wire = topo.wires.__next__() if PY3 else topo.wires.next()

    wires_from_edge = [i for i in topo.wires_from_edge(edg)]
    assert (len(wires_from_edge) == topo.number_of_wires_from_edge(edg))

    edges_from_wire = [i for i in topo.edges_from_wire(wire)]
    assert (len(edges_from_wire) == topo.number_of_edges_from_wire(wire))


def test_vertex_edge(topo):
    r"""

    Parameters
    ----------
    topo : aocutils.topology.Topo
        Topo object (pytest fixture)

    """
    vert = topo.vertices.__next__() if PY3 else topo.vertices.next()
    edge = topo.edges.__next__() if PY3 else topo.edges.next()

    verts_from_edge = [i for i in topo.vertices_from_edge(edge)]
    assert (len(verts_from_edge) == topo.number_of_vertices_from_edge(edge))

    edges_from_vert = [i for i in topo.edges_from_vertex(vert)]
    assert (len(edges_from_vert) == topo.number_of_edges_from_vertex(vert))


def test_vertex_face(topo):
    r"""

    Parameters
    ----------
    topo : aocutils.topology.Topo
        Topo object (pytest fixture)

    """
    vert = topo.vertices.__next__() if PY3 else topo.vertices.next()
    face = topo.faces.__next__() if PY3 else topo.faces.next()

    faces_from_vertex = [i for i in topo.faces_from_vertex(vert)]
    assert (len(faces_from_vertex) == topo.number_of_faces_from_vertex(vert))

    verts_from_face = [i for i in topo.vertices_from_face(face)]
    assert (len(verts_from_face) == topo.number_of_vertices_from_face(face))


def test_face_solid(topo):
    r"""

    Parameters
    ----------
    topo : aocutils.topology.Topo
        Topo object (pytest fixture)

    """
    face = topo.faces.__next__() if PY3 else topo.faces.next()
    solid = topo.solids.__next__() if PY3 else topo.solids.next()

    faces_from_solid = [i for i in topo.faces_from_solids(solid)]
    assert (len(faces_from_solid) == topo.number_of_faces_from_solids(solid))

    solids_from_face = [i for i in topo.solids_from_face(face)]
    assert (len(solids_from_face) == topo.number_of_solids_from_face(face))


def test_wire_face(topo):
    r"""

    Parameters
    ----------
    topo : aocutils.topology.Topo
        Topo object (pytest fixture)

    """
    wire = topo.wires.__next__() if PY3 else topo.wires.next()
    face = topo.faces.__next__() if PY3 else topo.faces.next()

    faces_from_wire = [i for i in topo.faces_from_wire(wire)]
    assert (len(faces_from_wire) == topo.number_of_faces_from_wires(wire))

    wires_from_face = [i for i in topo.wires_from_face(face)]
    assert (len(wires_from_face) == topo.number_of_wires_from_face(face))


def test_edges_out_of_scope(topo):
    r"""check pointers going out of scope

    Parameters
    ----------
    topo : aocutils.topology.Topo
        Topo object (pytest fixture)

    """
    face = topo.faces.__next__() if PY3 else topo.faces.next()
    _edges = list()
    for edg in aocutils.topology.Topo(face).edges:
        _edges.append(edg)
    for edg in _edges:
        assert not edg.IsNull()


def test_wires_out_of_scope(topo):
    r"""check pointers going out of scope

    Parameters
    ----------
    topo : aocutils.topology.Topo
        Topo object (pytest fixture)

    """
    wire = topo.wires.__next__() if PY3 else topo.wires.next()
    _edges, _vertices = list(), list()
    for edg in aocutils.topology.WireExplorer(wire).ordered_edges:
        _edges.append(edg)
    for edg in _edges:
        assert not edg.IsNull()
    for vert in aocutils.topology.WireExplorer(wire).ordered_vertices:
        _vertices.append(vert)
    for v in _vertices:
        assert not v.IsNull()
