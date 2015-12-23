#!/usr/bin/python
# coding: utf-8

r"""Points interpolation examples"""

import logging

import OCC.Display.SimpleGui
import OCC.gp

import aocutils.operations.interpolate
import aocutils.geom.curve
import aocutils.display.defaults

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s :: %(levelname)6s :: %(module)20s :: %(lineno)3d :: %(message)s')

backend = aocutils.display.defaults.backend
display, start_display, add_menu, add_function_to_menu = OCC.Display.SimpleGui.init_display(backend)

point_1 = OCC.gp.gp_Pnt(0, 0, 0)
point_2 = OCC.gp.gp_Pnt(10, 0, 0)
point_3 = OCC.gp.gp_Pnt(10, 10, 0)
point_list = [point_1, point_2, point_3]

vector_1 = OCC.gp.gp_Vec(1, 0, 0)
vector_2 = OCC.gp.gp_Vec(0, 1, 0)
vector_3 = OCC.gp.gp_Vec(0, 1, 0)
vector_list = [vector_1, vector_2, vector_3]

handle_points_to_bspline = aocutils.operations.interpolate.points_to_bspline(point_list)

handle_points = aocutils.operations.interpolate.points(point_list, vector_1, vector_3)

handle_points_vectors = aocutils.operations.interpolate.points_vectors(point_list, vector_list)

handle_points_no_tangency = aocutils.operations.interpolate.points_no_tangency(point_list)

handle_points_no_tangency_closed = aocutils.operations.interpolate.points_no_tangency(point_list, closed=True)


display.DisplayShape(aocutils.geom.curve.Curve.from_handle(handle_points_to_bspline).to_edge())
display.DisplayShape(aocutils.geom.curve.Curve.from_handle(handle_points).to_edge(), color="BLUE")
display.DisplayShape(aocutils.geom.curve.Curve.from_handle(handle_points_vectors).to_edge(), color="YELLOW")
display.DisplayShape(aocutils.geom.curve.Curve.from_handle(handle_points_no_tangency).to_edge(), color="PINK")
display.DisplayShape(aocutils.geom.curve.Curve.from_handle(handle_points_no_tangency_closed).to_edge(), color="WHITE")
for point in point_list:
    display.DisplayShape(point)
display.FitAll()
start_display()

