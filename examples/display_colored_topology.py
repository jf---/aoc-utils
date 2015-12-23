#!/usr/bin/python
# coding: utf-8

r"""
"""

import logging

import OCC.BRepPrimAPI
import OCC.Display.SimpleGui
import OCC.gp
import OCC.TopoDS
import OCC.BRep

import aocutils.display.defaults
# import aocutils.display.display
import aocutils.display.color
import aocutils.display.topology
import aocutils.mesh

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s :: %(levelname)6s :: %(module)20s :: %(lineno)3d :: %(message)s')

backend = aocutils.display.defaults.backend
display, start_display, add_menu, add_function_to_menu = OCC.Display.SimpleGui.init_display(backend)

box_x_dim = 10.
box_y_dim = 20.
box_z_dim = 30.


def box_shape():
    r"""Box shape for testing as a pytest fixture"""
    return OCC.BRepPrimAPI.BRepPrimAPI_MakeBox(box_x_dim, box_y_dim, box_z_dim).Shape()


def sphere_shape():
    r"""Box shape for testing as a pytest fixture"""
    shape = OCC.BRepPrimAPI.BRepPrimAPI_MakeSphere(OCC.gp.gp_Pnt(50, 0, 0), 10).Shape()
    aocutils.mesh.mesh(shape)
    return shape


def compound():
    r"""Create and return a compound from box and sphere"""
    # Create a compound
    compound = OCC.TopoDS.TopoDS_Compound()
    builder = OCC.BRep.BRep_Builder()
    builder.MakeCompound(compound)
    # Populate the compound
    builder.Add(compound, box_shape())
    builder.Add(compound, sphere_shape())
    return compound


def box_faces(event=None):
    display.EraseAll()
    # display.GetView().GetObject().SetBackgroundColor(aocutils.display.color.white)
    aocutils.display.topology.faces(display, box_shape())
    display.FitAll()


def box_edges(event=None):
    display.EraseAll()
    # display.GetView().GetObject().SetBackgroundColor(aocutils.display.color.white)
    aocutils.display.topology.edges(display, box_shape(), width=6)
    display.FitAll()


def box_wires(event=None):
    display.EraseAll()
    # display.GetView().GetObject().SetBackgroundColor(aocutils.display.color.white)
    aocutils.display.topology.wires(display, box_shape(), width=6)
    display.FitAll()


def sphere_faces(event=None):
    display.EraseAll()
    # display.GetView().GetObject().SetBackgroundColor(aocutils.display.color.white)
    aocutils.display.topology.faces(display, sphere_shape(),
                                    color_sequence=aocutils.display.color.spectral_color_sequence)
    display.FitAll()


def sphere_edges(event=None):
    display.EraseAll()
    # display.GetView().GetObject().SetBackgroundColor(aocutils.display.color.white)
    aocutils.display.topology.edges(display, sphere_shape(), width=6,
                                    color_sequence=aocutils.display.color.spectral_color_sequence)
    display.FitAll()


def compound_solids(event=None):
    display.EraseAll()
    aocutils.display.topology.solids(display, compound(), color_sequence=aocutils.display.color.spectral_color_sequence)
    display.FitAll()


add_menu('box')
add_function_to_menu('box', box_edges)
add_function_to_menu('box', box_faces)
add_function_to_menu('box', box_wires)
add_menu('sphere')
add_function_to_menu('sphere', sphere_edges)
add_function_to_menu('sphere', sphere_faces)
add_menu('compound')
add_function_to_menu('compound', compound_solids)
start_display()
