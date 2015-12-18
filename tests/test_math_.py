#!/usr/bin/python
# coding: utf-8

r"""
"""

import numpy as np

import OCC.gp

import aocutils.math_

list_numbers = [np.random.random() for _ in range(100)]
# list_gp_pnt = [OCC.gp.gp_Pnt(np.random.random(), np.random.random(), np.random.random()) for _ in range(100)]

print(list_numbers)
# print(list_gp_pnt)


def test_roundlist():
    list_rounded_numbers = aocutils.math_.roundlist(list_numbers, 3)
    assert len(list_rounded_numbers) == 100

def test_smooth_pnts():
    smoothed_numbers = aocutils.math_.smooth_pnts(list_numbers)
    assert len(smoothed_numbers) == 100
    # smoothed_points = occutils.math_.smooth_pnts(list_gp_pnt)

