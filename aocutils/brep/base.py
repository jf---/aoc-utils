# coding: utf-8

r"""base.py module of occutils

Classes
-------
BaseObject

"""

import logging

import OCC.BRepBuilderAPI
import OCC.BRepCheck
import OCC.BRepGProp
import OCC.Display.SimpleGui
import OCC.GProp
import OCC.TopoDS

import aocutils.common
import aocutils.types
import aocutils.topology
import aocutils.analyze.distance
import aocutils.display.display
import aocutils.brep.vertex_make
import aocutils.tolerance

logger = logging.getLogger(__name__)


class BaseObject(object):
    """Base class for all objects

    Parameters
    ----------
    wrapped_instance : TopoDS_Shape or subclass

    """
    def __init__(self, wrapped_instance, name=None, tolerance=aocutils.tolerance.OCCUTILS_DEFAULT_TOLERANCE):
        self._wrapped_instance = wrapped_instance
        self.name = name
        self.tolerance = tolerance

    @property
    def wrapped_instance(self):
        return self._wrapped_instance

    @property
    def tshape(self):
        r"""Wrapped instance TShape

        Returns
        -------
        OCC.TopoDS.TopoDS_TShape

        """
        return self._wrapped_instance.TShape()

    @property
    def location(self):
        r"""Wrapped instance Location

        Returns
        -------
        OCC.TopLoc.TopLoc_Location

        """
        return self._wrapped_instance.Location()

    @property
    def orientation(self):
        r"""Wrapped instance

        Returns
        -------
        PCC.TopABs.TopAbs_Orientation

        """
        return self._wrapped_instance.Orientation()

    @property
    def topo(self):
        r"""Topo

        Returns
        -------
        occutils.topology.Topo

        """
        return aocutils.topology.Topo(self._wrapped_instance)

    @property
    def topo_type(self):
        r"""Topological geom_type"""
        return aocutils.types.topo_types_dict[self._wrapped_instance.ShapeType()]

    # def check(self):
    #     """Check"""
    #     # _check = dict(vertex=OCC.BRepCheck.BRepCheck_Vertex, edge=OCC.BRepCheck.BRepCheck_Edge,
    #     #               wire=OCC.BRepCheck.BRepCheck_Wire, face=OCC.BRepCheck.BRepCheck_Face,
    #     #               shell=OCC.BRepCheck.BRepCheck_Shell)
    #     # _check[self.topo_type]
    #     # BRepCheck will be able to inform *what* actually is the matter,
    #     # though implementing this still is a bit of work...
    #     raise NotImplementedError

    @property
    def is_valid(self):
        r"""Checks that the shape is valid

        References
        ----------
        http://www.opencascade.com/doc/occt-6.9.0/refman/html/
        class_b_rep_check___analyzer.html#a8bfc5e0f53f16106fdfaf3e2c28c7cb0

        Returns
        -------
        bool
            True if the object is valid, False otherwise
        """
        analyse = OCC.BRepCheck.BRepCheck_Analyzer(self._wrapped_instance)
        ok = analyse.IsValid()
        if ok:
            return True
        else:
            return False

    def copy(self):
        r"""Copy

        Returns
        -------
        A copy of self

        """
        brep_builder_copy = OCC.BRepBuilderAPI.BRepBuilderAPI_Copy(self._wrapped_instance)
        brep_builder_copy.Perform(self._wrapped_instance)
        # get the class, construct a new instance
        # cast the cp.Shape() to its specific TopoDS topology
        _copy = self.__class__(aocutils.topology.shape_to_topology(brep_builder_copy.Shape()))
        return _copy

    def distance(self, other):
        """Minimum distance

        Parameters
        ----------
        other : any TopoDS_*
            The other TopoDS_* object

        Returns
         -------
        minimum distance, minimum distance points on shp1, minimum distance points on shp2

        """
        return aocutils.analyze.distance.MinimumDistance(self._wrapped_instance, other).minimum_distance

    def __eq__(self, other):
        return self._wrapped_instance.IsEqual(other)

    def __ne__(self, other):
        return not self.__eq__(other)
