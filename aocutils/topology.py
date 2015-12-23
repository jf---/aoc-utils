# coding: utf-8

r"""topology module of aocutils

Summary
-------
Topological analysis of Shapes

"""

from __future__ import print_function

import logging

import OCC.BRep
import OCC.BRepTools
import OCC.TopAbs
import OCC.TopExp
import OCC.TopTools
import OCC.TopoDS

import aocutils.exceptions
import aocutils.types

logger = logging.getLogger(__name__)

# __all__ = ['Topo', 'WireExplorer', 'dump_topology']


def shape_to_topology(shape):
    r"""Cast a TopoDS_Shape to its subtype determined by ShapeType()

    Parameters
    ----------
    shape : OCC.TopoDS.TopoDS_Shape

    """
    if isinstance(shape, OCC.TopoDS.TopoDS_Shape):
        return aocutils.types.topo_factory[shape.ShapeType()](shape)
    else:
        msg = 'shape is not a TopoDS_Shape'
        logger.error(msg)
        raise AttributeError(msg)


class WireExplorer(object):
    """Wire traversal

    Parameters
    ----------
    wire
    """
    def __init__(self, wire):
        # assert isinstance(wire, OCC.TopoDS.TopoDS_Wire), 'not a TopoDS_Wire'
        if not isinstance(wire, OCC.TopoDS.TopoDS_Wire):
            msg = 'Need a TopoDS_Wire, got a %s' % wire.__class__
            logger.critical(msg)
            raise aocutils.exceptions.WrongTopologicalType(msg)
        self.wire = wire
        self.wire_explorer = OCC.BRepTools.BRepTools_WireExplorer(self.wire)
        self.done = False

    def _reinitialize(self):
        self.wire_explorer = OCC.BRepTools.BRepTools_WireExplorer(self.wire)
        self.done = False

    def _loop_topo(self, edges=True):
        if self.done:
            self._reinitialize()
        topology_type = OCC.TopoDS.topods_Edge if edges else OCC.TopoDS.topods_Vertex
        python_list_of_shape = list()
        hashes = list()  # list that stores hashes to avoid redundancy
        toptools_list_of_shape = OCC.TopTools.TopTools_ListOfShape()
        while self.wire_explorer.More():
            # loop edges
            if edges:
                current_item = self.wire_explorer.Current()
            # loop vertices
            else:
                current_item = self.wire_explorer.CurrentVertex()
            current_item_hash = current_item.__hash__()
            if current_item_hash not in hashes:
                hashes.append(current_item_hash)
                toptools_list_of_shape.Append(current_item)
            self.wire_explorer.Next()

        # Convert occ_seq to python list
        occ_iterator = OCC.TopTools.TopTools_ListIteratorOfListOfShape(toptools_list_of_shape)
        while occ_iterator.More():
            topo_to_add = topology_type(occ_iterator.Value())
            python_list_of_shape.append(topo_to_add)
            occ_iterator.Next()
        self.done = True
        return iter(python_list_of_shape)

    @property
    def ordered_edges(self):
        r"""Ordered edges"""
        return self._loop_topo()

    @property
    def ordered_vertices(self):
        r"""Ordered vertices"""
        return self._loop_topo(edges=False)


class Topo(object):
    r"""Topology traversal.

    Implements topology traversal from any TopoDS_Shape.
    The Topo class lets you find how various topological entities are connected from one to another
    find the faces connected to an edge, find the vertices this edge is made from, get all faces connected to
    a vertex, and find out how many topological elements are connected from a source

    Notes
    -----

    When traversing TopoDS_Wire entities, its advised to use the specialized WireExplorer class,
    which will return the vertices / edges in the expected order

    For instance, a cube has 24 edges, 4 edges for each of 6 faces that results in 48 vertices,
    while there are only 8 vertices that have a unique geometric coordinate.

    In certain cases ( computing a graph from the topology ) its preferable to return topological entities
    that share similar geometry, though differ in orientation by setting the ``_ignore_orientation`` variable
    to True, in case of a cube, just 12 edges and only 8 vertices will be returned

    See Also
    --------
    TopoDS_Shape IsEqual / IsSame methods

    Parameters
    ----------
    my_shape : OCC.TopoDS.TopoDS_Shape or subclass
        the shape which topology will be traversed
    ignore_orientation : bool
        filter out TopoDS_* entities of similar TShape but different Orientation
    return_iter : bool
        If True, return iterators. If False, return lists

    """

    def __init__(self, my_shape, ignore_orientation=False, return_iter=True):
        self._my_shape = my_shape
        self._ignore_orientation = ignore_orientation
        self._return_iter = return_iter

    def _loop_topo(self, topology_type, topological_entity=None, topology_type_to_avoid=None):
        """Iterating over shape topology

        Notes
        -----
        this could be a faces generator for a python TopoShape class
        that way you can just do:
        for face in srf.faces:
            processFace(face)

        Parameters
        ----------
        topology_type
        topological_entity
        topology_type_to_avoid

        Returns
        -------
        list of TopoDS_*
            Depending on the topology_type input

        """
        # topo_types = {OCC.TopAbs.TopAbs_VERTEX: OCC.TopoDS.TopoDS_Vertex,
        #               OCC.TopAbs.TopAbs_EDGE: OCC.TopoDS.TopoDS_Edge,
        #               OCC.TopAbs.TopAbs_FACE: OCC.TopoDS.TopoDS_Face,
        #               OCC.TopAbs.TopAbs_WIRE: OCC.TopoDS.TopoDS_Wire,
        #               OCC.TopAbs.TopAbs_SHELL: OCC.TopoDS.TopoDS_Shell,
        #               OCC.TopAbs.TopAbs_SOLID: OCC.TopoDS.TopoDS_Solid,
        #               OCC.TopAbs.TopAbs_COMPOUND: OCC.TopoDS.TopoDS_Compound,
        #               OCC.TopAbs.TopAbs_COMPSOLID: OCC.TopoDS.TopoDS_CompSolid}

        # assert topology_type in topo_types.keys(), '%s not one of %s' % (topology_type, topo_types.keys())
        if topology_type not in aocutils.types.topo_type_class.keys():
            msg = '%s not one of %s' % (topology_type, aocutils.types.topo_type_class.keys())
            logger.critical(msg)
            raise aocutils.exceptions.WrongTopologicalType(msg)

        self.topexp_explorer = OCC.TopExp.TopExp_Explorer()
        # use self._my_shape if nothing is specified
        if topological_entity is None and topology_type_to_avoid is None:
            self.topexp_explorer.Init(self._my_shape, topology_type)

        elif topological_entity is None and topology_type_to_avoid is not None:
            self.topexp_explorer.Init(self._my_shape, topology_type, topology_type_to_avoid)

        elif topology_type_to_avoid is None:
            self.topexp_explorer.Init(topological_entity, topology_type)

        elif topology_type_to_avoid:
            self.topexp_explorer.Init(topological_entity, topology_type, topology_type_to_avoid)

        seq = list()
        hashes = list()  # list that stores hashes to avoid redundancy
        occ_seq = OCC.TopTools.TopTools_ListOfShape()
        while self.topexp_explorer.More():
            current_item = self.topexp_explorer.Current()
            current_item_hash = current_item.__hash__()

            if current_item_hash not in hashes:
                hashes.append(current_item_hash)
                occ_seq.Append(current_item)

            self.topexp_explorer.Next()
        # Convert occ_seq to python list
        occ_iterator = OCC.TopTools.TopTools_ListIteratorOfListOfShape(occ_seq)
        while occ_iterator.More():
            topo_to_add = aocutils.types.topo_factory[topology_type](occ_iterator.Value())
            seq.append(topo_to_add)
            occ_iterator.Next()

        if self._ignore_orientation:
            # filter out those entities that share the same TShape but do *not* share the same orientation
            filter_orientation_seq = list()
            for i in seq:
                _present = False
                for j in filter_orientation_seq:
                    if i.IsSame(j):
                        _present = True
                        break
                if _present is False:
                    filter_orientation_seq.append(i)
            return filter_orientation_seq
        else:
            if self._return_iter:
                return iter(seq)  # iterator
            else:
                return seq  # list

    @property
    def faces(self):
        """Loops over all faces"""
        return self._loop_topo(topology_type=OCC.TopAbs.TopAbs_FACE)

    @staticmethod
    def _number_of_topo(iterable):
        r"""Number of items in an iterable

        Parameters
        ----------
        iterable
            An iterable

        Returns
        -------
        int
            The number of items in the iterable
        """
        # n = 0
        # for i in iterable:
        #     n += 1
        # return n
        return len(list(iterable))

    @property
    def number_of_faces(self):
        r"""Number of faces"""
        return self._number_of_topo(self.faces)

    @property
    def vertices(self):
        r"""Loops over all vertices"""
        return self._loop_topo(OCC.TopAbs.TopAbs_VERTEX)

    @property
    def number_of_vertices(self):
        r"""Number of vertices"""
        return self._number_of_topo(self.vertices)

    @property
    def edges(self):
        r"""Loops over all edges"""
        return self._loop_topo(OCC.TopAbs.TopAbs_EDGE)

    @property
    def number_of_edges(self):
        r"""Number of edges"""
        return self._number_of_topo(self.edges)

    @property
    def wires(self):
        r"""Loops over all wires"""
        return self._loop_topo(OCC.TopAbs.TopAbs_WIRE)

    @property
    def number_of_wires(self):
        r"""Number of wires"""
        return self._number_of_topo(self.wires)

    @property
    def shells(self):
        r"""Loops over all shells"""
        return self._loop_topo(topology_type=OCC.TopAbs.TopAbs_SHELL)

    @property
    def number_of_shells(self):
        r"""Number of shells"""
        return self._number_of_topo(self.shells)

    @property
    def solids(self):
        r"""Loops over all solids"""
        return self._loop_topo(topology_type=OCC.TopAbs.TopAbs_SOLID)

    @property
    def number_of_solids(self):
        r"""Number of solids"""
        return self._number_of_topo(self.solids)

    @property
    def comp_solids(self):
        r"""Loops over all compound solids"""
        return self._loop_topo(OCC.TopAbs.TopAbs_COMPSOLID)

    @property
    def number_of_comp_solids(self):
        r"""Number of compound solids"""
        return self._number_of_topo(self.comp_solids)

    @property
    def compounds(self):
        r"""Loops over all compounds"""
        return self._loop_topo(OCC.TopAbs.TopAbs_COMPOUND)

    @property
    def number_of_compounds(self):
        r"""Number of compounds"""
        return self._number_of_topo(self.compounds)

    @staticmethod
    def ordered_vertices_from_wire(wire):
        r"""

        Parameters
        ----------
        wire : TopoDS_Wire

        Returns
        -------
        iterable

        """
        return WireExplorer(wire).ordered_vertices

    def number_of_ordered_vertices_from_wire(self, wire):
        r"""Number of ordered vertices from wire

        Parameters
        ----------
        wire

        Returns
        -------
        int

        """
        return self._number_of_topo(self.ordered_vertices_from_wire(wire))

    @staticmethod
    def ordered_edges_from_wire(wire):
        r"""

        Parameters
        ----------
        wire : TopoDS_Wire

        Returns
        -------
        iterable

        """
        we = WireExplorer(wire)
        return we.ordered_edges

    def number_of_ordered_edges_from_wire(self, wire):
        r"""Number of ordered edges from wire

        Parameters
        ----------
        wire

        Returns
        -------
        int

        """
        return self._number_of_topo(self.ordered_edges_from_wire(wire))

    def _map_shapes_and_ancestors(self, topo_type_a, topo_type_b, topological_entity):
        """Mapping of shapes to ancestors

        If you want to know how many edges a faces has:  _map_shapes_ancestors(self, TopAbs_EDGE, TopAbs_FACE, edg)
        will return the edges a faces has.

        Parameters
        ----------
        topo_type_a
        topo_type_b
        topological_entity : the entity from which to map

        Returns
        -------
        iter
            Iterator over the ancestor shapes

        """
        topo_set = set()
        _map = OCC.TopTools.TopTools_IndexedDataMapOfShapeListOfShape()
        OCC.TopExp.topexp_MapShapesAndAncestors(self._my_shape, topo_type_a, topo_type_b, _map)
        results = _map.FindFromKey(topological_entity)
        if results.IsEmpty():
            yield None

        topology_iterator = OCC.TopTools.TopTools_ListIteratorOfListOfShape(results)

        while topology_iterator.More():
            topo_entity = aocutils.types.topo_factory[topo_type_b](topology_iterator.Value())
            # return the entity if not in set to insure we're not returning entities several times
            if topo_entity not in topo_set:
                if self._ignore_orientation:
                    unique = True
                    for i in topo_set:
                        if i.IsSame(topo_entity):
                            unique = False
                            break
                    if unique:
                        yield topo_entity
                else:
                    yield topo_entity

            topo_set.add(topo_entity)
            topology_iterator.Next()

    def _number_shapes_ancestors(self, topo_type_a, topo_type_b, topological_entity):
        r"""Number of shape ancestors

        If you want to know how many edges a faces has:  _number_shapes_ancestors(self, TopAbs_EDGE, TopAbs_FACE, edg)
        will return the number of edges a faces has

        Parameters
        ----------
        topo_type_a
        topo_type_b
        topological_entity

        Returns
        -------
        int
            The number of shape ancestors
        """
        topo_set = set()
        _map = OCC.TopTools.TopTools_IndexedDataMapOfShapeListOfShape()
        OCC.TopExp.topexp_MapShapesAndAncestors(self._my_shape, topo_type_a, topo_type_b, _map)
        results = _map.FindFromKey(topological_entity)
        if results.IsEmpty():
            return None  # left as is on purpose, maybe 0 would be a better return value
        topology_iterator = OCC.TopTools.TopTools_ListIteratorOfListOfShape(results)
        while topology_iterator.More():
            topo_set.add(topology_iterator.Value())
            topology_iterator.Next()
        return len(topo_set)

    # ======================================================================
    # Edge <-> Face
    # ======================================================================
    def faces_from_edge(self, edge):
        r"""Faces that use an Edge

        Parameters
        ----------
        edge : TopoDS_Edge

        Returns
        -------
        list of OCC.TopAbs.TopAbs_FACE
        """
        return self._map_shapes_and_ancestors(topo_type_a=OCC.TopAbs.TopAbs_EDGE, topo_type_b=OCC.TopAbs.TopAbs_FACE,
                                              topological_entity=edge)

    def number_of_faces_from_edge(self, edge):
        r"""Number of faces that use an Edge

        Parameters
        ----------
        edge

        Returns
        -------
        int
        """
        return self._number_shapes_ancestors(topo_type_a=OCC.TopAbs.TopAbs_EDGE, topo_type_b=OCC.TopAbs.TopAbs_FACE,
                                             topological_entity=edge)

    def edges_from_face(self, face):
        r"""Edges used by a Face

        Parameters
        ----------
        face

        Returns
        -------
        list od TopoDS_Edge

        """
        return self._loop_topo(topology_type=OCC.TopAbs.TopAbs_EDGE, topological_entity=face)

    def number_of_edges_from_face(self, face):
        r"""Number of edges used by a Face

        Parameters
        ----------
        face

        Returns
        -------
        int

        """
        cnt = 0
        for _ in self._loop_topo(OCC.TopAbs.TopAbs_EDGE, face):
            cnt += 1
        return cnt

    # ======================================================================
    # Vertex <-> Edge
    # ======================================================================
    def vertices_from_edge(self, edg):
        r"""

        Parameters
        ----------
        edg

        Returns
        -------

        """
        return self._loop_topo(topology_type=OCC.TopAbs.TopAbs_VERTEX, topological_entity=edg)

    def number_of_vertices_from_edge(self, edg):
        r"""

        Parameters
        ----------
        edg

        Returns
        -------
        int

        """
        cnt = 0
        for _ in self._loop_topo(topology_type=OCC.TopAbs.TopAbs_VERTEX, topological_entity=edg):
            cnt += 1
        return cnt

    def edges_from_vertex(self, vertex):
        r"""

        Parameters
        ----------
        vertex

        Returns
        -------

        """
        return self._map_shapes_and_ancestors(topo_type_a=OCC.TopAbs.TopAbs_VERTEX, topo_type_b=OCC.TopAbs.TopAbs_EDGE,
                                              topological_entity=vertex)

    def number_of_edges_from_vertex(self, vertex):
        r"""

        Parameters
        ----------
        vertex

        Returns
        -------
        int

        """
        return self._number_shapes_ancestors(topo_type_a=OCC.TopAbs.TopAbs_VERTEX, topo_type_b=OCC.TopAbs.TopAbs_EDGE,
                                             topological_entity=vertex)

    # ======================================================================
    # Wire <-> Edge
    # ======================================================================
    def edges_from_wire(self, wire):
        r"""

        Parameters
        ----------
        wire

        Returns
        -------

        """
        return self._loop_topo(topology_type=OCC.TopAbs.TopAbs_EDGE, topological_entity=wire)

    def number_of_edges_from_wire(self, wire):
        r"""

        Parameters
        ----------
        wire

        Returns
        -------
        int

        """
        cnt = 0
        for _ in self._loop_topo(topology_type=OCC.TopAbs.TopAbs_EDGE, topological_entity=wire):
            cnt += 1
        return cnt

    def wires_from_edge(self, edg):
        r"""

        Parameters
        ----------
        edg

        Returns
        -------

        """
        return self._map_shapes_and_ancestors(topo_type_a=OCC.TopAbs.TopAbs_EDGE, topo_type_b=OCC.TopAbs.TopAbs_WIRE,
                                              topological_entity=edg)

    def wires_from_vertex(self, edg):
        r"""

        Parameters
        ----------
        edg

        Returns
        -------

        """
        return self._map_shapes_and_ancestors(topo_type_a=OCC.TopAbs.TopAbs_VERTEX, topo_type_b=OCC.TopAbs.TopAbs_WIRE,
                                              topological_entity=edg)

    def number_of_wires_from_edge(self, edg):
        r"""

        Parameters
        ----------
        edg

        Returns
        -------
        int
        """
        return self._number_shapes_ancestors(topo_type_a=OCC.TopAbs.TopAbs_EDGE, topo_type_b=OCC.TopAbs.TopAbs_WIRE,
                                             topological_entity=edg)

    # ======================================================================
    # Wire <-> Face
    # ======================================================================
    def wires_from_face(self, face):
        r"""

        Parameters
        ----------
        face

        Returns
        -------

        """
        return self._loop_topo(topology_type=OCC.TopAbs.TopAbs_WIRE, topological_entity=face)

    def number_of_wires_from_face(self, face):
        r"""

        Parameters
        ----------
        face

        Returns
        -------
        int

        """
        cnt = 0
        for _ in self._loop_topo(topology_type=OCC.TopAbs.TopAbs_WIRE, topological_entity=face):
            cnt += 1
        return cnt

    def faces_from_wire(self, wire):
        r"""

        Parameters
        ----------
        wire

        Returns
        -------

        """
        return self._map_shapes_and_ancestors(topo_type_a=OCC.TopAbs.TopAbs_WIRE, topo_type_b=OCC.TopAbs.TopAbs_FACE,
                                              topological_entity=wire)

    def number_of_faces_from_wires(self, wire):
        r"""

        Parameters
        ----------
        wire

        Returns
        -------

        """
        return self._number_shapes_ancestors(topo_type_a=OCC.TopAbs.TopAbs_WIRE, topo_type_b=OCC.TopAbs.TopAbs_FACE,
                                             topological_entity=wire)

    # ======================================================================
    # Vertex <-> Face
    # ======================================================================
    def faces_from_vertex(self, vertex):
        r"""

        Parameters
        ----------
        vertex

        Returns
        -------

        """
        return self._map_shapes_and_ancestors(topo_type_a=OCC.TopAbs.TopAbs_VERTEX, topo_type_b=OCC.TopAbs.TopAbs_FACE,
                                              topological_entity=vertex)

    def number_of_faces_from_vertex(self, vertex):
        r"""

        Parameters
        ----------
        vertex

        Returns
        -------

        """
        return self._number_shapes_ancestors(topo_type_a=OCC.TopAbs.TopAbs_VERTEX, topo_type_b=OCC.TopAbs.TopAbs_FACE,
                                             topological_entity=vertex)

    def vertices_from_face(self, face):
        r"""

        Parameters
        ----------
        face

        Returns
        -------

        """
        return self._loop_topo(topology_type=OCC.TopAbs.TopAbs_VERTEX, topological_entity=face)

    def number_of_vertices_from_face(self, face):
        r"""

        Parameters
        ----------
        face

        Returns
        -------
        int

        """
        cnt = 0
        for _ in self._loop_topo(topology_type=OCC.TopAbs.TopAbs_VERTEX, topological_entity=face):
            cnt += 1
        return cnt

    # ======================================================================
    # Face <-> Solid
    # ======================================================================
    def solids_from_face(self, face):
        r"""

        Parameters
        ----------
        face

        Returns
        -------

        """
        return self._map_shapes_and_ancestors(topo_type_a=OCC.TopAbs.TopAbs_FACE, topo_type_b=OCC.TopAbs.TopAbs_SOLID,
                                              topological_entity=face)

    def number_of_solids_from_face(self, face):
        r"""

        Parameters
        ----------
        face

        Returns
        -------
        int

        """
        return self._number_shapes_ancestors(topo_type_a=OCC.TopAbs.TopAbs_FACE, topo_type_b=OCC.TopAbs.TopAbs_SOLID,
                                             topological_entity=face)

    def faces_from_solids(self, solid):
        r"""

        Parameters
        ----------
        solid

        Returns
        -------

        """
        return self._loop_topo(topology_type=OCC.TopAbs.TopAbs_FACE, topological_entity=solid)

    def number_of_faces_from_solids(self, solid):
        r"""

        Parameters
        ----------
        solid

        Returns
        -------

        """
        cnt = 0
        for _ in self._loop_topo(topology_type=OCC.TopAbs.TopAbs_FACE, topological_entity=solid):
            cnt += 1
        return cnt
