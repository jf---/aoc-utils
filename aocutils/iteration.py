# coding: utf-8

r"""iteration.py module of occutils

This module helps looping through topology

Classes
-------
    EdgePairsFromWire
        next()
        __iter__()
    LoopWirePairs
        closest_point()
        next()
        __iter__()

"""

import OCC.BRep

import aocutils.topology
import aocutils.brep.edge


class EdgePairsFromWire(object):
    r"""Helper class to loop through a wire and return ordered pairs of edges

    Parameters
    ----------
    wire

    """
    def __init__(self, wire):
        self.wire = wire
        self.edge_pairs = list()
        self.prev_edge = None
        self.we = aocutils.topology.WireExplorer(self.wire).ordered_edges()
        self.number_of_edges = self.we.__length_hint__()
        self.previous_edge = None
        self.current_edge = None
        self.first_edge = None
        self.index = 0

    def next(self):
        r"""

        Returns
        -------

        """
        if self.index == 0:
            # first edge, need to set self.previous_edge
            self.previous_edge = self.we.next()
            self.current_edge = self.we.next()
            self.first_edge = self.previous_edge   # for the last iteration
            self.index += 1
            return [self.previous_edge, self.current_edge]
        elif self.index == self.number_of_edges-1:
            # no next edge
            self.index += 1
            return [self.current_edge, self.first_edge]
        else:
            self.previous_edge = self.current_edge
            self.current_edge = self.we.next()
            self.index += 1
            return [self.previous_edge, self.current_edge]

    def __iter__(self):
        return self


class LoopWirePairs(object):
    r"""For looping through consecutive wires assures that the returned edge pairs are ordered

    Parameters
    ----------
    wire_a
    wire_b

    """
    def __init__(self, wire_a, wire_b):
        self.wireA = wire_a
        self.wireB = wire_b
        self.we_A = aocutils.topology.WireExplorer(self.wireA)
        self.we_B = aocutils.topology.WireExplorer(self.wireB)
        self.tp_A = aocutils.topology.Topo(self.wireA)
        self.tp_B = aocutils.topology.Topo(self.wireB)
        self.bt = OCC.BRep.BRep_Tool()
        self.vertsA = [v for v in self.we_A.ordered_vertices()]
        self.vertsB = [v for v in self.we_B.ordered_vertices()]

        self.edgesA = [v for v in aocutils.topology.WireExplorer(wire_a).ordered_edges()]
        self.edgesB = [v for v in aocutils.topology.WireExplorer(wire_b).ordered_edges()]

        self.pntsB = [self.bt.Pnt(v) for v in self.vertsB]
        self.number_of_vertices = len(self.vertsA)
        self.index = 0

    def closest_point(self, vertex_from_wire_a):
        r"""

        Parameters
        ----------
        vertex_from_wire_a

        Returns
        -------

        """
        pt = self.bt.Pnt(vertex_from_wire_a)
        distances = [pt.Distance(i) for i in self.pntsB]
        indx_max_dist = distances.index(min(distances))
        return self.vertsB[indx_max_dist]

    def next(self):
        r"""

        Returns
        -------

        """
        if self.index == self.number_of_vertices:
            raise StopIteration

        vert = self.vertsA[self.index]
        closest = self.closest_point(vert)
        edges_a = self.tp_A.edges_from_vertex(vert)
        edges_b = self.tp_B.edges_from_vertex(closest)
        a1, a2 = aocutils.brep.edge.Edge(edges_a.next()), aocutils.brep.edge.Edge(edges_a.next())
        b1, b2 = aocutils.brep.edge.Edge(edges_b.next()), aocutils.brep.edge.Edge(edges_b.next())
        mp_a = a1.mid_point()[1]
        self.index += 1

        if mp_a.Distance(b1.mid_point()[1]) < mp_a.Distance(b2.mid_point()[1]):
            return iter([a1, a2]), iter([b1, b2])
        else:
            return iter([a1, a2]), iter([b2, b1])

    def __iter__(self):
        return self
