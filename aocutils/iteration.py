# coding: utf-8

r"""iteration.py module

Summary
-------

This module helps looping through topology

"""

import OCC.BRep

import aocutils.topology
import aocutils.brep.edge


class EdgePairsFromWire(object):
    r"""Helper class to loop through a wire and return ordered pairs of edges

    Parameters
    ----------
    wire : OCC.TopoDS.TopoDS_Wire

    """
    def __init__(self, wire):
        self.wire = wire
        self.edge_pairs = list()
        self.prev_edge = None
        self.wire_explorer = aocutils.topology.WireExplorer(self.wire).ordered_edges()
        self.number_of_edges = self.wire_explorer.__length_hint__()
        self.previous_edge = None
        self.current_edge = None
        self.first_edge = None
        self.index = 0

    def next(self):
        r"""next() method to make EdgePairsFromWire an iterable

        Returns
        -------

        """
        if self.index == 0:
            # first edge, need to set self.previous_edge
            self.previous_edge = self.wire_explorer.next()
            self.current_edge = self.wire_explorer.next()
            self.first_edge = self.previous_edge   # for the last iteration
            self.index += 1
            return [self.previous_edge, self.current_edge]
        elif self.index == self.number_of_edges-1:
            # no next edge
            self.index += 1
            return [self.current_edge, self.first_edge]
        else:
            self.previous_edge = self.current_edge
            self.current_edge = self.wire_explorer.next()
            self.index += 1
            return [self.previous_edge, self.current_edge]

    def __iter__(self):
        return self


class LoopWirePairs(object):
    r"""For looping through consecutive wires assures that the returned edge pairs are ordered

    Parameters
    ----------
    wire_a : OCC.TopoDS.TopoDS_Wire
    wire_b : OCC.TopoDS.TopoDS_Wire

    """
    def __init__(self, wire_a, wire_b):
        self.wireA = wire_a
        self.wireB = wire_b
        self.wire_explorer_a = aocutils.topology.WireExplorer(self.wireA)
        self.wire_explorer_b = aocutils.topology.WireExplorer(self.wireB)
        self.topo_a = aocutils.topology.Topo(self.wireA)
        self.topo_b = aocutils.topology.Topo(self.wireB)
        self.brep_tool = OCC.BRep.BRep_Tool()
        self.vertices_a = [v for v in self.wire_explorer_a.ordered_vertices()]
        self.vertices_b = [v for v in self.wire_explorer_b.ordered_vertices()]

        self.edges_a = [v for v in aocutils.topology.WireExplorer(wire_a).ordered_edges()]
        self.edges_b = [v for v in aocutils.topology.WireExplorer(wire_b).ordered_edges()]

        self.pnts_b = [self.brep_tool.Pnt(v) for v in self.vertices_b]
        self.number_of_vertices = len(self.vertices_a)
        self.index = 0

    def closest_point(self, vertex_from_wire_a):
        r"""Closest vertex in the wire b to a vertex from wire a

        Parameters
        ----------
        vertex_from_wire_a

        Returns
        -------
        OCC.TopoDS.TopoDS_Vertex

        """
        pt = self.brep_tool.Pnt(vertex_from_wire_a)
        distances = [pt.Distance(i) for i in self.pnts_b]
        indx_max_dist = distances.index(min(distances))
        return self.vertices_b[indx_max_dist]

    def next(self):
        r"""next() method to make LoopWirePairs an iterable

        Returns
        -------

        """
        if self.index == self.number_of_vertices:
            raise StopIteration

        vert = self.vertices_a[self.index]
        closest = self.closest_point(vert)
        edges_a = self.topo_a.edges_from_vertex(vert)
        edges_b = self.topo_b.edges_from_vertex(closest)
        edge_a1, edge_a2 = aocutils.brep.edge.Edge(edges_a.next()), aocutils.brep.edge.Edge(edges_a.next())
        edge_b1, edge_b2 = aocutils.brep.edge.Edge(edges_b.next()), aocutils.brep.edge.Edge(edges_b.next())
        mp_a = edge_a1.mid_point()[1]
        self.index += 1

        if mp_a.Distance(edge_b1.mid_point()[1]) < mp_a.Distance(edge_b2.mid_point()[1]):
            return iter([edge_a1, edge_a2]), iter([edge_b1, edge_b2])
        else:
            return iter([edge_a1, edge_a2]), iter([edge_b2, edge_b1])

    def __iter__(self):
        return self
