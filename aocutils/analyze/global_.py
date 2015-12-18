#!/usr/bin/python
# coding: utf-8

r"""analyze/global_.py
"""

import logging

import OCC.GProp
import OCC.BRepGProp

import aocutils.tolerance
import aocutils.analyze.bounds
import aocutils.types
import aocutils.exceptions

import aocutils.tolerance

logger = logging.getLogger(__name__)


class GlobalProperties(object):
    r"""Global properties for all topologies

    Parameters
    ----------
    shape : OCC.TopoDS.TopoDS_Shape

    """

    linear_types = ["edge", "wire"]
    surfacic_types = ["face", "shell"]
    volumic_types = ["solid"]

    def __init__(self, shape):
        self.shape = shape
        self._topo_type = aocutils.types.topo_lut[self.shape.ShapeType()]
        self._system = None

    @property
    def topo_type(self):
        r"""Topological geom_type"""
        return self._topo_type

    @property
    def system(self):
        r"""Initialise the GProp_GProps depending on the topological geom_type

        Notes
        -----
        geom_type could be abstracted with TopoDS... instead of using _topo_type

        Returns
        -------
        OCC.GProp.GProp_GProps

        """
        self._system = OCC.GProp.GProp_GProps()

        if self._topo_type in GlobalProperties.surfacic_types:
            OCC.BRepGProp.brepgprop_SurfaceProperties(self.shape, self._system)
        elif self._topo_type in GlobalProperties.linear_types:
            OCC.BRepGProp.brepgprop_LinearProperties(self.shape, self._system)
        elif self._topo_type in GlobalProperties.volumic_types:
            OCC.BRepGProp.brepgprop_VolumeProperties(self.shape, self._system)
        return self._system

    def centre(self):
        r"""Centre of the entity

        Returns
        -------
        """
        return self.system.CentreOfMass()

    def inertia(self):
        """Inertia matrix"""
        return self.system.MatrixOfInertia(), self.system.MomentOfInertia()

    def area(self):
        r"""Area of the surface"""
        if self.topo_type not in GlobalProperties.surfacic_types:
            msg = "area is only defined for linear surfacic types"
            logger.error(msg)
            raise aocutils.exceptions.WrongTopologicalType(msg)
        return self._mass()

    def volume(self):
        r"""Volume"""
        if self.topo_type not in GlobalProperties.volumic_types:
            msg = "volume is only defined for linear volumic types"
            logger.error(msg)
            raise aocutils.exceptions.WrongTopologicalType(msg)
        return self._mass()

    def _mass(self):
        return self.system.Mass()

    def length(self):
        r"""length of a wire or edge"""
        if self.topo_type not in GlobalProperties.linear_types:
            msg = "length is only defined for linear topological types"
            logger.error(msg)
            raise aocutils.exceptions.WrongTopologicalType(msg)
        return self.system.Mass()
