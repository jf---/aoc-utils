#!/usr/bin/python
# coding: utf-8

r"""edge.py module example use

Box -> Topology -> 1 edge -> edge tolerance

"""

from __future__ import print_function

import OCC.BRepPrimAPI
import OCC.Display.SimpleGui

import aocutils.brep.edge
import aocutils.topology
import aocutils.display.display

display, start_display, add_menu, add_function_to_menu = OCC.Display.SimpleGui.init_display("wx")


if __name__ == '__main__':
    box = OCC.BRepPrimAPI.BRepPrimAPI_MakeBox(10, 20, 30).Shape()
    box_topology = aocutils.topology.Topo(box)
    first_edge = next(box_topology.edges)
    occutils_wrapped_edge = aocutils.brep.edge.Edge(first_edge)

    sphere = OCC.BRepPrimAPI.BRepPrimAPI_MakeSphere(10).Shape()
    sphere_topology = aocutils.topology.Topo(sphere, return_iter=False)
    print(sphere_topology.number_of_edges)
    edges = sphere_topology.edges
    edge_sphere_0 = edges[0]
    edge_sphere_1 = edges[1]
    edge_sphere_2 = edges[2]
    wrapped_edge_sphere = aocutils.brep.edge.Edge(edge_sphere_1)

    print(occutils_wrapped_edge.tolerance)
    display.DisplayShape(edge_sphere_1)
    display.DisplayShape(wrapped_edge_sphere.parameter_to_point(5.))
    display.DisplayShape(wrapped_edge_sphere.parameter_to_point(6.))
    # occutils.display.display.Display("wx").display_shape(first_edge)
    # occutils.display.display.Display("wx").display_shape(first_edge_sphere)
    display.FitAll()
    start_display()
