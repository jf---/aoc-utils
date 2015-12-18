# coding: utf-8

r"""solid module of occutils

Classes
-------
Solid
    check()
    shells()

"""

import logging

import OCC.BRepBuilderAPI
import OCC.BRepOffsetAPI
import OCC.TopoDS
import OCC.BRepCheck

import aocutils.topology
import aocutils.brep.base
import aocutils.brep.shell
import aocutils.brep.wire
import aocutils.brep.edge
import aocutils.brep.face
import aocutils.operations.transform
import aocutils.analyze.global_
import aocutils.exceptions

logger = logging.getLogger(__name__)


class Solid(aocutils.brep.base.BaseObject):
    r"""Solid class

    Parameters
    ----------
        topods_solid : OCC.TopoDS.TopoDS_Solid

    """
    def __init__(self, topods_solid):
        if not isinstance(topods_solid, OCC.TopoDS.TopoDS_Solid):
            msg = 'need a TopoDS_Solid, got a %s' % topods_solid.__class__
            logger.critical(msg)
            raise aocutils.exceptions.WrongTopologicalType(msg)
        assert not topods_solid.IsNull()
        aocutils.brep.base.BaseObject.__init__(self, topods_solid, 'solid')

        # self.global_properties = occutils.analyze.global_.GlobalProperties(self)

    @property
    def topods_solid(self):
        return self._wrapped_instance

    def check(self):
        r"""Super class abstract method implementation"""
        # super(Solid, self).check()
        # todo : call BRepCheck_Face methods
        return OCC.BRepCheck.BRepCheck_Solid(self._wrapped_instance)

    def shells(self):
        r"""Shells making the solid

        Returns
        -------
        list[Shell]

        """
        return (aocutils.brep.shell.Shell(sh) for sh in aocutils.topology.Topo(self._wrapped_instance))
