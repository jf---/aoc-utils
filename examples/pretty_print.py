#!/usr/bin/python
# coding: utf-8

r"""pretty_print examples
"""


from __future__ import print_function

import math

import OCC.gp

import aocutils.primitives
import aocutils.pretty_print

point = OCC.gp.gp_Pnt(1, 2, 3)
print(aocutils.pretty_print.gp_pnt_print(point))

vec = OCC.gp.gp_Vec(1, 2, 3)
print(aocutils.pretty_print.gp_vec_print(vec))

dir = OCC.gp.gp_Dir(1, 2, 3)
ax1 = OCC.gp.gp_Ax1(point, dir)
print(aocutils.pretty_print.gp_ax1_print(ax1))


trsf = OCC.gp.gp_Trsf()
trsf.SetTranslation(vec)
print(aocutils.pretty_print.gp_trsf_print(trsf))

trsf.SetRotation(ax1, math.radians(180))
print(aocutils.pretty_print.gp_trsf_print(trsf))

box_shape = aocutils.primitives.box(10, 10, 10)
aocutils.pretty_print.dump_topology(box_shape)