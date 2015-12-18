#!/usr/bin/python
# coding: utf-8

r"""
"""

from __future__ import print_function

import aocutils.primitives
import aocutils.types
import aocutils.brep.solid
import aocutils.brep.solid_make
import aocutils.topology


box = aocutils.primitives.box(10, 10, 10)
sphere = aocutils.primitives.sphere(10)

print(type(box))
print(aocutils.types.topo_lut[box.ShapeType()])


solid = aocutils.topology.Topo(box).solids()[0]
print(type(solid))
wrapped_solid = aocutils.brep.solid.Solid(solid)
print(type(wrapped_solid))


