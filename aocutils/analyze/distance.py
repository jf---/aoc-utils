#!/usr/bin/python
# coding: utf-8

r"""distance
"""

import OCC.BRepExtrema

import aocutils.common


class MinimumDistance(object):
    r"""Minimum distance

    Parameters
    ----------
    shape_1 : Any OCC.topoDS.TopoDS_*
    shape_2 : Any OCC.topoDS.TopoDS_*

    """
    def __init__(self, shape_1, shape_2):
        dist_shape_shape = OCC.BRepExtrema.BRepExtrema_DistShapeShape(shape_1, shape_2)
        dist_shape_shape.Perform()

        with aocutils.common.AssertIsDone(dist_shape_shape, 'Failed computing minimum distances'):
            self._min_dist = dist_shape_shape.Value()
            self._points_pairs = list()
            self._nb_solutions = dist_shape_shape.NbSolution()
            for i in range(1, dist_shape_shape.NbSolution() + 1):
                self._points_pairs.append((dist_shape_shape.PointOnShape1(i), dist_shape_shape.PointOnShape2(i)))

    @property
    def minimum_distance(self):
        r"""Minimum distance between the 2 shapes

        Returns
        -------
        float

        """
        return self._min_dist

    @property
    def point_pairs(self):
        r"""Solution point pairs

        Returns
        -------
        list[tuple[OCC.gp.gp_Pnt]]"""
        assert self._nb_solutions == len(self._points_pairs)
        return self._points_pairs

    @property
    def nb_solutions(self):
        r"""Number of minimum distance solutions

        Returns
        -------
        int

        """
        assert self._nb_solutions == len(self._points_pairs)
        return self._nb_solutions
